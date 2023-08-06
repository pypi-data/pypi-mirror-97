"""REST client for the Waylay Platform."""

from collections import defaultdict
from typing import (
    Optional, TypeVar, List, Mapping, Type, Iterable, Dict
)

import pkg_resources

from .service import (
    WaylayService,
    WaylayServiceContext,
    AnalyticsService,
    ByomlService,
    TimeSeriesService,
    ApiService,
    StorageService,
    UtilService,
    ETLService,
)
from .exceptions import ConfigError

from .config import (
    WaylayConfig,
    DEFAULT_PROFILE
)
from .auth import (
    WaylayCredentials,
    ClientCredentials,
    TokenCredentials,
    DEFAULT_ACCOUNTS_URL
)

S = TypeVar('S', bound=WaylayService)


class WaylayClient():
    """REST client for the Waylay Platform."""

    analytics: AnalyticsService
    byoml: ByomlService
    config: WaylayConfig
    timeseries: TimeSeriesService
    api: ApiService
    storage: StorageService
    util: UtilService
    etl: ETLService

    @classmethod
    def from_profile(
        cls, profile: str = DEFAULT_PROFILE,
        interactive=True, accounts_url=DEFAULT_ACCOUNTS_URL
    ):
        """Create a WaylayClient named profile.

        Uses credentials from environment variables or a locally stored configuration.
        """
        return cls(WaylayConfig.load(profile, interactive=interactive, accounts_url=accounts_url))

    @classmethod
    def from_client_credentials(
        cls, api_key: str, api_secret: str, accounts_url: str = DEFAULT_ACCOUNTS_URL
    ):
        """Create a WaylayClient using the given client credentials."""
        return cls.from_credentials(ClientCredentials(api_key, api_secret, accounts_url))

    @classmethod
    def from_token(
        cls, token_string: str, accounts_url: str = DEFAULT_ACCOUNTS_URL
    ):
        """Create a WaylayClient using a waylay token."""
        return cls.from_credentials(TokenCredentials(token_string, accounts_url))

    @classmethod
    def from_credentials(
        cls, credentials: WaylayCredentials
    ):
        """Create a WaylayClient using the given client credentials."""
        return cls(WaylayConfig(credentials))

    def __init__(self, config: WaylayConfig):
        """Create a WaylayConfig instance."""
        self._services: List[WaylayService] = []
        self.config = config
        self.load_services()

    @property
    def services(self) -> List[WaylayService]:
        """Get the services that are available through this client."""
        return self._services

    @property
    def service_context(self) -> WaylayServiceContext:
        """Get the WaylayServiceContext view on this client."""
        return self

    def configure(self, config: WaylayConfig):
        """Update this client with the given configuration."""
        self.config = config
        for srv in self._services:
            srv.configure(self.config, context=self.service_context)

    def list_root_urls(self) -> Mapping[str, Optional[str]]:
        """List the currently configured root url for each of the registered services."""
        return {srv.config_key: srv.get_root_url() for srv in self._services}

    def __repr__(self):
        """Get a technical string representation of this instance."""
        return (
            f"<{self.__class__.__name__}("
            f"services=[{','.join(list(srv_class.service_key for srv_class in self.services))}],"
            f"config={self.config}"
            ")>"
        )

    def load_services(self):
        """Load all services that are registered with the `waylay_services` entry point."""
        registered_service_classes = [
            srv_class
            for entry_point in pkg_resources.iter_entry_points('waylay_services')
            for srv_class in entry_point.load()
        ]
        self.register_service(*registered_service_classes)

    def register_service(self, *service_class: Type[S]) -> Iterable[S]:
        """Create and initialize one or more service of the given class.

        Replaces any existing with the same service_key.
        """
        new_services = [srv_class() for srv_class in service_class]
        new_plugin_priorities: Dict[str, int] = defaultdict(int)
        for srv in new_services:
            new_plugin_priorities[srv.service_key] = max(
                srv.plugin_priority, new_plugin_priorities[srv.service_key]
            )

        # delete existing services
        to_delete_service_index = [
            idx for idx, srv in enumerate(self._services)
            if (
                srv.service_key in new_plugin_priorities and
                srv.plugin_priority <= new_plugin_priorities[srv.service_key]
            )
        ]

        for idx in reversed(to_delete_service_index):
            # delete indexed entries in list from the back
            del self._services[idx]

        # change service list
        for srv in new_services:
            if srv.plugin_priority == new_plugin_priorities[srv.service_key]:
                self._services.append(srv)
                setattr(self, srv.service_key, srv)

        # reconfigure
        self.configure(self.config)
        return new_services

    # implements WaylayServiceContext protocol
    def get(self, service_class: Type[S]) -> Optional[S]:
        """Get the service instance for the provided class, if it is registered.

        Implements the `WaylayServiceContext.get` protocol.
        """
        for srv in self._services:
            if isinstance(srv, service_class):
                return srv
        return None

    def require(self, service_class: Type[S]) -> S:
        """Get the service instance for the given class or raise a ConfigError.

        Implements the `WaylayServiceContext.require` protocol.
        """
        srv = self.get(service_class)
        if srv is None:
            raise ConfigError(f"service {service_class.__name__} is not available.")
        return srv

    def list(self) -> List[WaylayService]:
        """List all registered Services.

        Implements the `WaylayServiceContext.list` protocol.
        """
        return list(self._services)
