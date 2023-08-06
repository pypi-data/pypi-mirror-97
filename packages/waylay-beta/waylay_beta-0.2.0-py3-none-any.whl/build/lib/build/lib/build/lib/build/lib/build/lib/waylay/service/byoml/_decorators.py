"""Resource action method decorators specific for the 'byoml' service."""

from functools import wraps

from simple_rest_client.exceptions import ErrorWithResponse

from ._exceptions import (
    ByomlActionError
)


def byoml_exception_decorator(action_method):
    """Create a decorator that parses json error responses."""
    @wraps(action_method)
    def wrapped(*args, **kwargs):
        try:
            return action_method(*args, **kwargs)
        except ErrorWithResponse as exc:
            raise ByomlActionError.from_cause(exc) from exc
    return wrapped
