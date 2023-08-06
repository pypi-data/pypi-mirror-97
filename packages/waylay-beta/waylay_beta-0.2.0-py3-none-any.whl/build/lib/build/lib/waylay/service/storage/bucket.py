"""REST definitions for the 'bucket' entity of the 'storage' service."""
from urllib.parse import quote

from waylay.service import WaylayResource, decorators


class BucketResource(WaylayResource):
    """REST Resource for the 'bucket' entity of the 'storage' service."""

    link_roots = {
        'iodoc': '${iodoc_url}/api/storage/?id=',
        'apidoc':  '${root_url}/docs#/storage/',
        'openapi': '${root_url}/openapi.json'
    }

    actions = {
        'list': {
            'method': 'GET', 'url': '/bucket', 'decorators': [
                decorators.exception_decorator,
                decorators.return_path_decorator(['buckets']),
            ],
            'description': 'List available bucket aliases',
            'links': {
                'iodoc': 'list-bucket',
                'apidoc': 'list_buckets_bucket__get',
                'openapi': f"#/paths/{quote('/bucket')}/get"
            }
        },
        'get': {
            'method': 'GET', 'url': '/bucket/{}', 'decorators': [
                decorators.exception_decorator,
                decorators.return_body_decorator,
            ],
            'description': 'Get metadata for a specific bucket alias',
            'links': {
                'iodoc': 'get-bucket',
                'apidoc': 'get_bucket_bucket__bucket_name__get',
                'openapi': f"#/paths/{quote('/bucket/{bucket_name}')}/get"
            }
        },
    }
