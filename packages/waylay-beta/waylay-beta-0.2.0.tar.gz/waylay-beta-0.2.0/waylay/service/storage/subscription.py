"""REST definitions for the 'subscription' entity of the 'storage' service."""
from urllib.parse import quote

from waylay.service import WaylayResource
from waylay.service import decorators


class SubscriptionResource(WaylayResource):
    """REST Resource for the 'subscription' entity of the 'storage' service."""

    link_roots = {
        'iodoc': '${iodoc_url}/api/storage/?id=',
        'apidoc':  '${root_url}/docs#/subscription/',
        'openapi': '${root_url}/openapi.json'
    }
    actions = {
        'list': {
            'method': 'GET', 'url': '/subscription/{}', 'decorators': [
                decorators.exception_decorator,
                decorators.return_path_decorator(['subscriptions']),
            ],
            'description': 'List available subscriptions for a given bucket.',
            'links': {
                'iodoc': 'list-bucket-subscriptions',
                'apidoc': 'query_subscriptions_subscription__bucket_name__get',
                'openapi': f"#/paths/{quote('/subscription/{bucket_name}')}/get"
            }
        },
        'get': {
            'method': 'GET', 'url': '/subscription/{}/{}', 'decorators': [
                decorators.exception_decorator,
                decorators.return_body_decorator,
            ],
            'description': 'Retrieve the representation of a notification subscription.',
            'links': {
                'iodoc': 'get-subscription',
                'apidoc': 'get_subscription_subscription__bucket_name___id__get',
                'openapi': f"#/paths/{quote('/subscription/{bucket_name}/{id}')}/get"
            }
        },
        'create': {
            'method': 'POST', 'url': '/subscription/{}', 'decorators': [
                decorators.exception_decorator,
                decorators.return_body_decorator,
            ],
            'description': 'Create a new notification subscription.',
            'links': {
                'iodoc': 'create-subscription',
                'apidoc': 'post_subscription_subscription__bucket_name__post',
                'openapi': f"#/paths/{quote('/subscription/{bucket_name}/{id}')}/post"
            }
        },
        'replace': {
            'method': 'PUT', 'url': '/subscription/{}/{}', 'decorators': [
                decorators.exception_decorator,
                decorators.return_body_decorator,
            ],
            'description': 'Create or Replace the definition of a notification subscription.',
            'links': {
                'iodoc': 'update-subscription',
                'apidoc': 'put_subscription_subscription__bucket_name___id__put',
                'openapi': f"#/paths/{quote('/subscription/{bucket_name}/{id}')}/put"
            }
        },
        'remove': {
            'method': 'DELETE', 'url': '/subscription/{}/{}', 'decorators': [
                decorators.exception_decorator,
                decorators.return_body_decorator,
            ],
            'description': 'Remove a notification subscription.',
            'links': {
                'iodoc': 'delete-subscription',
                'apidoc': 'delete_subscription_subscription__bucket_name___id__delete',
                'openapi': f"#/paths/{quote('/subscription/{bucket_name}/{id}')}/delete"
            }

        },
        'remove_all': {
            'method': 'DELETE', 'url': '/subscription/{}', 'decorators': [
                decorators.exception_decorator,
                decorators.return_body_decorator,
            ],
            'description': 'Remove all notification subscription that satisfy a query.',
            'links': {
                'iodoc': 'delete-subscriptions',
                'apidoc': 'delete_subscriptions_subscription__bucket_name__delete',
                'openapi': f"#/paths/{quote('/subscription/{bucket_name}')}/delete"
            }
        },
    }
