"""REST definitions for version status of Waylay Storage service."""
from urllib.parse import quote
from waylay.service import WaylayResource, decorators

DEFAULT_DECORATORS = [decorators.exception_decorator, decorators.return_body_decorator]


class AboutResource(WaylayResource):
    """Static information about version."""

    link_roots = {
        'iodoc': '${iodoc_url}/api/storage/?id=',
        'apidoc':  '${root_url}/docs#/status/',
        'openapi': '${root_url}/openapi.json'
    }

    actions = {
        'version': {
            'method': 'GET',
            'url': '/',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Application version',
            'links': {
                'iodoc': 'version',
                'apidoc': 'version__get',
                'openapi': f"#/paths/{quote('/')}/get",
            },
        },
        'status': {
            'method': 'GET',
            'url': '/status',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Validation and statistics on the buckets and policies for this tenant.',
            'links': {
                'iodoc': 'tenant-status',
                'apidoc': 'status_status_get',
                'openapi': f"#/paths/{quote('/status')}/get",
            },
        },
    }
