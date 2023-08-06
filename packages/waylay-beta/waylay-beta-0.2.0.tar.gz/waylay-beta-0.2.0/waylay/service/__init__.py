"""Waylay Rest Services."""

from ._base import WaylayService, WaylayResource, WaylayServiceContext
from . import _decorators as decorators

from .analytics import AnalyticsService
from .byoml import ByomlService
from .timeseries import TimeSeriesService
from .api import ApiService
from .storage import StorageService
from .util import UtilService
from .etl import ETLService


SERVICES = [
    AnalyticsService,
    ByomlService,
    TimeSeriesService,
    ApiService,
    StorageService,
    UtilService,
    ETLService,
]
