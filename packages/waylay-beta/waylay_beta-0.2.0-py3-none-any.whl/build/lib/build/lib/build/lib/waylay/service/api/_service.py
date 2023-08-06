
"""REST client for the Waylay API Service (engine)."""

from typing import Optional
from waylay.service import WaylayService

from .resource import ResourceResource
from .resource_type import ResourceTypeResource
from .settings import SettingsResource


class ApiService(WaylayService):
    """REST client for the main Waylay Api Service (engine)."""

    config_key = 'api'
    service_key = 'api'
    default_root_url: Optional[str] = None  # will default to https://{token.domain}
    resource_definitions = {
        'settings': SettingsResource,
        'resource': ResourceResource,
        'resource_type': ResourceTypeResource
    }
    settings: SettingsResource
    resource: ResourceResource
    resource_type: ResourceTypeResource
