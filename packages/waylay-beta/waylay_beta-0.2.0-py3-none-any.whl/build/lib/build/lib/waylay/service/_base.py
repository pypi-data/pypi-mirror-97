"""Base classes for Waylay REST Services and Resources."""
__docformat__ = "google"

from typing import (
    Optional, Type, TypeVar,
    Mapping, List, Dict, Optional
)
try:
    from typing import Protocol
except ImportError:
    # typing.Protocol is a 3.8 feature ...
    # ... but typing_extensions provides forward compatibility.
    from typing_extensions import Protocol  # type: ignore

from string import Template

from simple_rest_client.api import Resource, API
from waylay.config import WaylayConfig
from waylay.exceptions import ConfigError

S = TypeVar('S', bound='WaylayService')
R = TypeVar('R', bound='WaylayResource')


class WaylayServiceContext(Protocol):
    """View protocol for the dynamic service context."""

    def get(self, service_class: Type[S]) -> Optional[S]:
        """Get the service instance for the given class, if available."""

    def require(self, service_class: Type[S]) -> S:
        """Get the service instances for the given class or raise a ConfigError."""

    def list(self) -> List['WaylayService']:
        """List all available service instances."""


DEFAULT_SEVICE_TIMEOUT = 10


# Implementation Note
# -------------------
# Current solution is scaffolded around the `simple_rest_client`, but is planned to be refactored.

class WaylayAction(dict):
    """Client object representing a Waylay REST action."""

    @property
    def resource(self) -> 'WaylayResource':
        """Get the parent resource of this action."""
        return self['_resource']

    @property
    def name(self) -> Optional[str]:
        """Get the action name."""
        return self.get('name', self.get('id'))

    @property
    def method(self) -> Optional[str]:
        """Get the action method."""
        return self.get('method')

    @property
    def url(self) -> Optional[str]:
        """Get the action url template."""
        return self.get('url')

    @property
    def description(self) -> Optional[str]:
        """Get the action description."""
        return self.get('description')

    @property
    def hal_links(self) -> Dict[str, Dict[str, str]]:
        """Get (documentation) links templates."""
        roots = self.resource.hal_roots
        return {
            link: dict(href=roots.get(link, '') + ref)
            for link, ref in self.get('links', {}).items()
        }


class WaylayResource(Resource):
    """Client object representing a Waylay REST Resource.

    This is a collection of REST operations that have a single Waylay Entity as subject.
    """

    service: 'WaylayService'

    # class variables
    link_roots: Dict[str, str] = {}

    def __init__(self, *args, **kwargs):
        """Create a Waylay Resource."""
        self.actions = {
            id: WaylayAction(id=id, _resource=self, **action)
            for id, action in self.actions.items()
        }
        super().__init__(*args, **kwargs)

    @property
    def name(self):
        """Get the name that identifies this resource in the Python SDK."""
        return self.resource_name

    @property
    def description(self):
        """Get a description of this service."""
        return self.__doc__

    def add_action(self, action_name: str):
        """Add action, and apply decorators."""
        super().add_action(action_name)
        self.decorate_action(action_name)

    def decorate_action(self, action_name):
        """Decorate the action if a 'decorators' definition exist."""
        action = self.get_action(action_name)
        decorators = action.get('decorators', None)
        if decorators:
            for decorator in decorators:
                setattr(self, action_name, decorator(getattr(self, action_name)))

    def __repr__(self):
        """Get a technical string representation of this action."""
        actions_repr = ', '.join(
            f"{name}: '{action_def['method']} {action_def['url']}'"
            for name, action_def in self.actions.items()
        )
        return (
            f"<{self.__class__.__name__}("
            f"actions=[{actions_repr}]"
            ")>"
        )

    @property
    def hal_roots(self) -> Dict[str, str]:
        """Get the root urls for documentation links if this resource."""
        return {
            link: Template(
                href_root
            ).safe_substitute(
                root_url=self.api_root_url,
                doc_url=self.service.config.DOC_URL,
                iodoc_url=self.service.config.IODOC_URL,
            )
            for link, href_root in self.link_roots.items()
        }

    def hal_links(self, action: Optional[str]) -> Dict[str, Dict[str, str]]:
        """Create a HAL `_links` representation for (documentation) links.

        Attributes:
            action      if specified, give links for a specific action rather than the resource.
        """
        hrefs = {rel: '' for rel in self.link_roots}
        if action:
            hrefs = self.actions.get(action).links

        return {
            link_rel: dict(
                href=Template(
                    href_root + hrefs.get(link_rel, '')
                ).safe_substitute(
                    root_url=self.api_root_url,
                    doc_url=self.service.config.DOC_URL,
                    iodoc_url=self.service.config.IODOC_URL,
                )
            )
            for link_rel, href_root in self.link_roots.items()
            if link_rel in hrefs
        }


class WaylayService(API):
    """Client object representing a Waylay Service.

    A collection of Resources with their operations.
    """

    config: WaylayConfig

    # class variables
    service_key: str = ''
    config_key: str = 'api'
    default_root_url: Optional[str] = None
    resource_definitions: Mapping[str, Type[Resource]] = {}
    plugin_priority = 0
    link_templates: Dict[str, str] = {}

    @property
    def name(self):
        """Get the name that identifies this service in the Python SDK."""
        return self.service_key

    @property
    def description(self):
        """Get a description of this service."""
        return self.__doc__

    @property
    def resources(self):
        """Get the REST resources supported by this service."""
        return self.list_resources()

    def __init__(self, *args, **kwargs):
        """Create a WaylayService."""
        timeout = kwargs.pop('timeout', DEFAULT_SEVICE_TIMEOUT)
        json_encode_body = kwargs.pop('json_encode_body', True)
        super().__init__(*args, timeout=timeout, json_encode_body=json_encode_body, **kwargs)
        for name, resource_class in self.resource_definitions.items():
            self._add_waylay_resource(resource_name=name, resource_class=resource_class)

    def _add_waylay_resource(self, resource_name: str, resource_class: Type[R], **kwargs) -> R:
        self.add_resource(resource_name=resource_name, resource_class=resource_class, **kwargs)
        waylay_resource: R = self._resources[self.correct_attribute_name(resource_name)]
        waylay_resource.service = self
        return waylay_resource

    def set_root_url(self, root_url):
        """Set the root url and reconfigure the service."""
        self.config.set_root_url(self.config_key, root_url)
        self.reconfigure()

    def get_root_url(self) -> Optional[str]:
        """Get the root url."""
        if self.config is None:
            return self.default_root_url
        return self.config.get_root_url(self.config_key, self.default_root_url)

    @property
    def root_url(self) -> Optional[str]:
        """Get the root url."""
        return self.get_root_url()

    def configure(self: S, config: WaylayConfig, context: WaylayServiceContext) -> S:
        """Configure endpoints and authentication with given configuration.

        Returns self
        """
        self.config = config
        return self.reconfigure()

    def reconfigure(self: S) -> S:
        """Configure endpoints and authentication with current configuration.

        Returns self
        """
        if self.config is None:
            return self
        root_url = self.get_root_url()
        if not root_url:
            raise ConfigError(
                f'The service `{self.service_key}` has no url configuration. '
                f'Please provide a endpoint using a setting with key `{self.config_key}`,'
                'or request your tenant administrator '
                f'to configure the global setting `waylay_{self.config_key}`.'
            )
        for resource in self._resources.values():
            resource.api_root_url = root_url
            resource.client.auth = self.config.auth
        return self

    def list_resources(self) -> List[WaylayResource]:
        """List the WaylayResources of this service."""
        return list(self._resources.values())

    def __repr__(self):
        """Get a technical string representation of this service."""
        return (
            f"<{self.__class__.__name__}("
            f"service_key={self.service_key},"
            f"config_key={self.config_key},"
            f"root_url={self.get_root_url()},"
            f"resources=[{', '.join(self._resources.keys())}]"
            ")>"
        )

    def hal_links(self) -> Dict[str, Dict[str, str]]:
        """Create a HAL `_links` representation for the documentation links."""
        return {
            rel: dict(href=Template(href).safe_substitute(
                root_url=self.root_url,
                doc_url=self.config.DOC_URL,
                iodoc_url=self.config.IODOC_URL,
            ))
            for rel, href in self.link_templates.items()
        }
