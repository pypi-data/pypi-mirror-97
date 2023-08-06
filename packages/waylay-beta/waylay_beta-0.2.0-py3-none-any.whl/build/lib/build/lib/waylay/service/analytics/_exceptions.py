"""Exceptions specific to the Analytics Service."""

from typing import (
    List, Mapping, Any
)
from ...exceptions import RestResponseError, RestResponseParseError


class AnalyticsActionError(RestResponseError):
    """Error that represents the json messages of a analytics response."""

    @property
    def messages(self) -> List[Mapping[str, Any]]:
        """Get the list of message objects returned by an analytics error response."""
        return self._get_from_body('messages', [])

    @property
    def message(self):
        """Get the main user error returned by an analytics error response."""
        return self._get_from_body('error', super().message)


class AnalyticsActionParseError(RestResponseParseError, AnalyticsActionError):
    """Indicates that a analytics response could not be parsed."""
