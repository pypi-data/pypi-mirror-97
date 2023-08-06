"""REST definitions for the resource entity of the api service."""

from waylay.service import WaylayResource
from waylay.service import decorators

DEFAULT_DECORATORS = [decorators.exception_decorator, decorators.return_body_decorator]


class ResourceResource(WaylayResource):
    """REST Resource for the `resource` entity of the `api` (resource provisioning) service."""

    link_roots = {
        'doc': '${doc_url}/api/resources/#',
        'iodoc': '${iodoc_url}/api/resources/?id='
    }

    actions = {
        'get': {
            'method': 'GET',
            'url': '/api/resources/{}',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Retrieve a `resource` representation.',
            'links': {
                'doc': 'retrieve-resource',
                'iodoc': 'retrieve-resource'
            },
        },
        'create': {
            'method': 'POST',
            'url': '/api/resources',
            'decorators': [
                decorators.exception_decorator,
                decorators.return_path_decorator(['entity'])
            ],
            'description': 'Create a `resource` entity.',
            'links': {
                'doc': 'create-resource',
                'iodoc': 'create-resource'
            },
        },
        'update': {
            'method': 'PATCH',
            'url': '/api/resources/{}',
            'decorators': DEFAULT_DECORATORS,
            'description': '(Partially) update a `resource` representation.',
            'links': {
                'doc': 'partial-resource-update',
                'iodoc': 'partial-resource-update'
            },
        },
        'replace': {
            'method': 'PUT',
            'url': '/api/resources/{}',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Replace a `resource` representation.',
            'links': {
                'doc': 'update-resource',
                'iodoc': 'update-resource'
            },
        },
        'remove': {
            'method': 'DELETE',
            'url': '/api/resources/{}',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Delete a `resource` entity.',
            'links': {
                'doc': 'delete-resource',
                'iodoc': 'delete-resource'
            },
        },
        'search': {
            'method': 'GET',
            'url': '/api/resources',
            'decorators': [
                decorators.exception_decorator,
                decorators.return_path_decorator(['values'])
            ],
            'description': 'Query `resource` entities.',
            'links': {
                'doc': 'query-resources',
                'iodoc': 'query-resources'
            },
        },
    }
