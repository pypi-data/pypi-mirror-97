"""REST definitions for the 'object' entity of the 'storage' service."""

import isodate
import re
from datetime import timedelta
from urllib.parse import urlsplit, parse_qs, quote
from functools import wraps

from typing import Union, Optional, Dict, Iterator

from waylay.service import WaylayResource
from waylay.service import decorators


def parse_expiry_params(expiry: Union[str, timedelta]) -> Dict[str, int]:
    """Parse sign expiry parameters.

    Input should be either:
    * an ISO period expression
    * a simple string expression `1d` , `6h`, `300s`
    * a `datetime.timedelta` objec
    """
    if expiry is None:
        return {}
    if isinstance(expiry, str):
        if 'P' in expiry:
            return parse_expiry_params(isodate.parse_duration(expiry))
        simple_period_match = re.match(r"(\d+)([dhs])", expiry)
        if simple_period_match:
            amount, dhs_key = simple_period_match.groups()
            key: str = dict(
                d='expiry_days', h='expiry_hours', s='expiry_seconds'
            )[dhs_key]
            return {key: int(amount)}

    if isinstance(expiry, timedelta):
        return {
            'expiry_days': expiry.days,
            'expiry_seconds': expiry.seconds
        }
    raise AttributeError(f'Not an expiry expression: {expiry}')


def _object_path_remove_path_suffix(action_method):
    # remove the `/` suffix from the (virtual folder) object_path,
    # as we already include it in the url template.
    @wraps(action_method)
    def wrapped(*args, **kwargs):
        new_args = args
        if args[1].endswith('/'):
            new_args = [args[1].rstrip('/'), *args[1:]]
        return action_method(*new_args, **kwargs)
    return wrapped


class FolderResource(WaylayResource):
    """REST Resource for the folder 'object' entity of the 'storage' service."""

    link_roots = {
        'iodoc': '${iodoc_url}/api/storage/?id=',
        'apidoc':  '${root_url}/docs#/storage/',
        'openapi': '${root_url}/openapi.json'
    }

    actions = {
        'list': {
            'method': 'GET', 'url': '/bucket/{}/{}/', 'decorators': [
                _object_path_remove_path_suffix,
                decorators.exception_decorator,
                decorators.return_path_decorator(
                    ['objects']
                ),
            ],
            'description': 'List objects in this folder.',
            'links': {
                'iodoc': 'list-object',
                'apidoc': 'list_or_get_objects_bucket__bucket_name___object_path__get',
                'openapi': f"#/paths/{quote('/bucket/{bucket_name}/{object_path}')}/get"
            }
        },
        'create': {
            'method': 'PUT', 'url': '/bucket/{}/{}/', 'decorators': [
                _object_path_remove_path_suffix,
                decorators.exception_decorator,
                decorators.return_body_decorator,
            ],
            'description': 'Create a folder.',
            'links': {
                'iodoc': 'put-folder',
                'apidoc': 'create_folder_bucket__bucket_name___object_path___put',
                'openapi': f"#/paths/{quote('/bucket/{bucket_name}/{object_path}/')}/put"
            }
        },
        'stat': {
            'method': 'GET', 'url': '/bucket/{}/{}/?stat=true', 'decorators': [
                _object_path_remove_path_suffix,
                decorators.exception_decorator,
                decorators.return_body_decorator,
            ],
            'description': 'Get the details of this folder',
            'links': {
                'iodoc': 'get-object',
                'apidoc': 'list_or_get_objects_bucket__bucket_name___object_path__get',
                'openapi': f"#/paths/{quote('/bucket/{bucket_name}/{object_path}')}/get"
            }
        },
        'remove': {
            'method': 'DELETE', 'url': '/bucket/{}/{}/', 'decorators': [
                _object_path_remove_path_suffix,
                decorators.exception_decorator,
                decorators.return_path_decorator(
                    ['_links']
                )
            ],
            'description': 'Remove this folder',
            'links': {
                'iodoc': 'delete-object-or-folder',
                'apidoc': 'delete_object_bucket__bucket_name___object_path__delete',
                'openapi': f"#/paths/{quote('/bucket/{bucket_name}/{object_path}')}/delete"
            }
        },
    }


class ObjectResource(WaylayResource):
    """REST Resource for the 'object' entity of the 'storage' service."""

    link_roots = {
        'iodoc': '${iodoc_url}/api/storage/?id=',
        'apidoc':  '${root_url}/docs#/storage/',
        'openapi': '${root_url}/openapi.json'
    }

    actions = {
        'sign_get': {
            'method': 'GET', 'url': '/bucket/{}/{}?sign=GET', 'decorators': [
                decorators.exception_decorator,
                decorators.return_path_decorator(
                    ['_links', 'get_object', 'href']
                ),
            ],
            'description': 'Create a signed http GET link for the given bucket and object path.',
            'links': {
                'iodoc': 'sign_url',
                'apidoc': 'list_or_get_objects_bucket__bucket_name___object_path__get',
                'openapi': f"#/paths/{quote('/subscription/{bucket_name}')}/get"
            }
        },
        'sign_post': {
            'method': 'GET', 'url': '/bucket/{}/{}?sign=POST', 'decorators': [
                decorators.exception_decorator,
                decorators.return_path_decorator(
                    ['_links', 'post_object']
                ),
            ],
            'description': 'Create a signed http POST link for the given bucket and object path.',
            'links': {
                'iodoc': 'sign_url',
                'apidoc': 'list_or_get_objects_bucket__bucket_name___object_path__get',
                'openapi': f"#/paths/{quote('/subscription/{bucket_name}')}/get"
            }
        },
        'sign_put': {
            'method': 'GET', 'url': '/bucket/{}/{}?sign=PUT', 'decorators': [
                decorators.exception_decorator,
                decorators.return_path_decorator(
                    ['_links', 'put_object', 'href']
                ),
            ],
            'description':  'Create a signed http PUT link for the given bucket and object path.',
            'links': {
                'iodoc': 'sign_url',
                'apidoc': 'list_or_get_objects_bucket__bucket_name___object_path__get',
                'openapi': f"#/paths/{quote('/subscription/{bucket_name}')}/get"
            }
        },
        'stat': {
            'method': 'GET', 'url': '/bucket/{}/{}?stat=true', 'decorators': [
                decorators.exception_decorator,
                decorators.return_body_decorator,
            ],
            'description': 'Get the object metadata for the given bucket and object path.',
            'links': {
                'iodoc': 'get-object',
                'apidoc': 'list_or_get_objects_bucket__bucket_name___object_path__get',
                'openapi': f"#/paths/{quote('/subscription/{bucket_name}')}/get"
            }
        },
        'remove': {
            'method': 'DELETE', 'url': '/bucket/{}/{}', 'decorators': [
                decorators.exception_decorator,
                decorators.return_body_decorator
            ],
            'description': 'Remove the object at the given bucket and object path.',
            'links': {
                'iodoc': 'delete-object-or-folder',
                'apidoc': 'delete_object_bucket__bucket_name___object_path__delete',
                'openapi': f"#/paths/{quote('/subscription/{bucket_name}')}/get"
            }
        },
        'list': {
            'method': 'GET', 'url': '/bucket/{}/{}', 'decorators': [
                decorators.exception_decorator,
                decorators.return_path_decorator(
                    ['objects']
                ),
            ],
            'description': 'List objects in given bucket with a given path prefix.',
            'links': {
                'iodoc': 'list-object',
                'apidoc': 'list_or_get_objects_bucket__bucket_name___object_path__get',
                'openapi': f"#/paths/{quote('/subscription/{bucket_name}')}/get"
            }
        },
    }

    def iter_list_all(self, bucket: str, prefix: str, params: Optional[Dict] = None) -> Iterator[Dict]:
        """Use paging to iterate over all objects."""
        done = False
        while not done:
            result = self.list(bucket, prefix, select_path=[], params=params)  # pylint: disable=no-member
            for object in result.get('objects', []):
                yield object
            next_link = result.get('_links', {}).get('next')
            if next_link:
                query = urlsplit(next_link['href']).query
                params = {k: v[0] for k, v in parse_qs(query, keep_blank_values=True).items()}
            else:
                done = True
