"""REST definitions for the 'resource_type' entity of the 'api' service."""

from waylay.service import WaylayResource
from waylay.service import decorators

DEFAULT_DECORATORS = [decorators.exception_decorator, decorators.return_body_decorator]


class ResourceTypeResource(WaylayResource):
    """REST Resource for the 'resource_type' entity of the 'api' resource provisioning service."""

    link_roots = {
        'doc': '${doc_url}/api/resources/#',
        'iodoc': '${iodoc_url}/api/resources/?id='
    }

    actions = {
        'create': {
            'method': 'POST',
            'url': '/api/resourcetypes',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Create a `resource type` entity.',
            'links': {
                'doc': 'create-resource-type',
                'iodoc': 'create-resource-type'
            },
        },
        'remove': {
            'method': 'DELETE',
            'url': '/api/resourcetypes/{}',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Delete a `resource type` entity.',
            'links': {
                'doc': 'delete-resource-type',
                'iodoc': 'delete-resource-type'
            },
        },
        'replace': {
            'method': 'PUT',
            'url': '/api/resourcetypes/{}',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Replace a `resource type` representation.',
            'links': {
                'doc': 'update-resource-type',
                'iodoc': 'update-resource-type'
            },
        },
        'update': {
            'method': 'PATCH',
            'url': '/api/resourcetypes/{}',
            'decorators': DEFAULT_DECORATORS,
            'description': '(Partially) update a `resource type` representation.',
            'links': {
                'doc': 'partial-resource-type-update',
                'iodoc': 'partial-resource-type-update'
            },
        },
        'get': {
            'method': 'GET',
            'url': '/api/resourcetypes/{}',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Retrieve a `resource type` representation.',
            'links': {
                'doc': 'retrieve-resource-type',
                'iodoc': 'retrieve-resource-type'
            },
        },
        'list': {
            'method': 'GET',
            'url': '/api/resourcetypes',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Query `resource type` entities.',
            'links': {
                'doc': 'query-resource-types',
                'iodoc': 'query-resource-types'
            },
        },
    }
