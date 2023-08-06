"""REST definitions for the import process entity of the etl service."""

from waylay.service import WaylayResource
from waylay.service import decorators

DEFAULT_DECORATORS = [decorators.exception_decorator, decorators.return_body_decorator]


class ImportResource(WaylayResource):
    """REST Resource for the import process entity of the etl service."""

    link_roots = {
        'iodoc': '${iodoc_url}/features/etl/?id='
    }

    actions = {
        'initiate': {
            'method': 'POST',
            'url': '/api/etl/import',
            'decorators': DEFAULT_DECORATORS,
            'description': "Initiates an etl import process as specified in the request body.",
            'links': {
                'iodoc': 'etl-import-service',
            }
        },
        'get': {
            'method': 'GET',
            'url': '/api/etl/import',
            'decorators': DEFAULT_DECORATORS,
            'description': "Retrieves the last or active etl import process.",
            'links': {
                'iodoc': 'etl-import-service',
            }
        }
    }
