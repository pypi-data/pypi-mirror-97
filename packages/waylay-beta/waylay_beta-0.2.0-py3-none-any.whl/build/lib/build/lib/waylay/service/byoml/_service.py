
"""REST client for the Waylay Time Series Analytics Service."""

from .._base import WaylayService

from .model import ModelResource
from .about import AboutResource


class ByomlService(WaylayService):
    """REST client for the Waylay BYOML Service."""

    service_key = 'byoml'
    config_key = 'byoml'
    default_root_url = 'https://byoml.waylay.io'

    resource_definitions = {
        'model': ModelResource,
        'about': AboutResource
    }

    model: ModelResource
    about: AboutResource
