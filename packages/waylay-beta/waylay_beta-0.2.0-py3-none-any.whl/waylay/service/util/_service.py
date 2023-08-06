
"""Utility tools and services for the Python SDK."""

from waylay.service import WaylayService, WaylayServiceContext
from waylay.config import WaylayConfig

from .info import InfoTool


class UtilService(WaylayService):
    """Utility Service for the python SDK."""

    service_key = 'util'

    info: InfoTool

    def configure(self, config: WaylayConfig, context: WaylayServiceContext) -> 'UtilService':
        """Configure endpoints and authentication with given config."""
        self.config = config
        self.info = InfoTool(context)
        return self.reconfigure()

    def reconfigure(self) -> 'UtilService':
        """Reconfigure this service after a configuration change."""
        return self
