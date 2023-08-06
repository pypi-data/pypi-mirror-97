
"""REST client for the Waylay Time Series Analytics Service."""

from .._base import WaylayService

from .query import QueryResource
from .about import AboutResource


class AnalyticsService(WaylayService):
    """REST client for the Analytics Service."""

    service_key = 'analytics'
    config_key = 'analytics'
    default_root_url = 'https://ts-analytics.waylay.io'
    resource_definitions = {
        'query': QueryResource,
        'about': AboutResource
    }
    query: QueryResource
    about: AboutResource

    def __init__(self):
        """Create an AnlayticsService."""
        super().__init__(
            json_encode_body=True,
            params={
                'api_version': '0.19',
                # 'render.mode': 'RENDER_MODE_SERIES', // conflicts with 'Accept: text/csv' !! bug?
                # 'json_validate_request': True
            }
        )
