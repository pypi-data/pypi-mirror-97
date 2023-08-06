"""Internal service with tools for timeseries import and export."""

from waylay.service import WaylayService, WaylayServiceContext
from waylay.config import WaylayConfig
from waylay.service.storage import StorageService
from waylay.service.etl import ETLService
from waylay.service.api import ApiService
from waylay.service.analytics import AnalyticsService

from .tool import TimeSeriesETLTool


class TimeSeriesService(WaylayService):
    """Tool service the timeseries import and export operations."""

    service_key = 'timeseries'

    etl_tool: TimeSeriesETLTool

    def configure(self, config: WaylayConfig, context: WaylayServiceContext) -> 'TimeSeriesService':
        """Configure endpoints and authentication with given config."""
        self.config = config
        self.etl_tool = TimeSeriesETLTool(
            context.require(StorageService),
            context.require(ETLService),
            context.require(ApiService),
            context.require(AnalyticsService),
        )
        return self.reconfigure()

    def reconfigure(self) -> 'TimeSeriesService':
        """Reconfigure after configuration change."""
        return self
