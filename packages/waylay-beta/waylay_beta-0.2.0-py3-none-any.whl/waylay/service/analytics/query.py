"""Definitions for the 'query' entity of the 'analytics' Service."""

from .._base import WaylayResource
from .._decorators import (
    return_path_decorator
)
from ._decorators import (
    analytics_exception_decorator,
    analytics_return_dataframe_decorator,
    MultiFrameHandling
)


def parse_query_entity(json_dict: dict):
    """Get the default response constructor for query config entities."""
    return json_dict


CONFIG_ENTITY_DECORATORS = [
    analytics_exception_decorator,
    return_path_decorator(['query'], parse_query_entity)
]

CONFIG_LIST_DECORATORS = [
    analytics_exception_decorator,
    return_path_decorator(['queries', 'name'])
]

DATA_RESPONSE_DECORATORS = [
    analytics_exception_decorator,
    analytics_return_dataframe_decorator(
        'data',
        default_frames_handling=MultiFrameHandling.JOIN
    )
]


class QueryResource(WaylayResource):
    """REST Resource for the 'query' entity of the 'analytics' Service."""

    link_roots = {
        'doc': '${doc_url}/api/query/',
        'iodoc': '${iodoc_url}/api/query/',
        'apidoc':  '${root_url}/apidocs/'
    }

    actions = {
        'list': {
            'method': 'GET',
            'url': '/config/query',
            'decorators': CONFIG_LIST_DECORATORS,
            'description': 'List or search <em>Query Configurations</em>.',
            'links': {
                'doc': 'search/#search',
                'iodoc': '?id=data-query-search-api',
                'apidoc': '#/query%20config/get_config_query'
            }
        },
        'create': {
            'method': 'POST',
            'url': '/config/query',
            'decorators': CONFIG_ENTITY_DECORATORS,
            'description': 'Create a new <em>Query Configuration</em>.',
            'links': {
                'doc': 'crud/#create',
                'iodoc': '?id=create',
                'apidoc': '#/query%20config/post_config_query'
            }
        },
        'get': {
            'method': 'GET',
            'url': '/config/query/{}',
            'decorators': CONFIG_ENTITY_DECORATORS,
            'description': 'Fetch the named <em>Query Configuration</em>.',
            'links': {
                'doc': 'crud/#retrieve',
                'iodoc': '?id=retrieve',
                'apidoc': '#/query%20config/get_config_query__query_name_'
            }
        },
        'remove': {
            'method': 'DELETE',
            'url': '/config/query/{}',
            'decorators': [analytics_exception_decorator],
            'description': 'Remove the named <em>Query Configuration</em>.',
            'links': {
                'doc': 'crud/#delete',
                'iodoc': '?id=delete',
                'apidoc': '#/query%20config/delete_config_query__query_name_'
            }
        },
        'replace': {
            'method': 'PUT',
            'url': '/config/query/{}',
            'decorators': CONFIG_ENTITY_DECORATORS,
            'description': 'Replace the named <em>Query Configuration</em>.',
            'links': {
                'doc': 'crud/#replace',
                'iodoc': '?id=replace',
                'apidoc': '#/query%20config/put_config_query__query_name_'
            }
        },
        'data': {
            'method': 'GET',
            'url': '/data/query/{}',
            'decorators': DATA_RESPONSE_DECORATORS,
            'description': (
                'Execute the timeseries query specified by the named <em>Query Configuration</em>.'
            ),
            'links': {
                'doc': 'data/#query-execution',
                'iodoc': '?id=query-execution',
                'apidoc': '#/data/get_data_query__query_name_'
            }
        },
        'execute': {
            'method': 'POST',
            'url': '/data/query',
            'decorators': DATA_RESPONSE_DECORATORS,
            'description': 'Execute the timeseries query specified in the request body.',
            'links': {
                'doc': 'data/#query-execution',
                'iodoc': '?id=query-execution',
                'apidoc': '#/data/post_data_query'
            }
        },
    }
