"""REST definitions for the Settings entity of the Waylay Engine Service."""

from waylay.service import WaylayResource
from waylay.service import decorators


DEFAULT_DECORATORS = [decorators.exception_decorator, decorators.return_body_decorator]


class SettingsResource(WaylayResource):
    """REST Resource for the `settings` entity of the provisioning API."""

    actions = {
        'get': {
            'method': 'GET', 'url': '/api/settings',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Retrieve tenant global settings.',
            'links': {
            },
        },
    }
