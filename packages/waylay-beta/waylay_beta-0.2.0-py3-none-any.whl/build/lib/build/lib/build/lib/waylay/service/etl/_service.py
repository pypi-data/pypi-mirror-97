"""REST client for the Waylay ETL Service."""

from waylay.service import WaylayService

from .import_ import ImportResource


class ETLService(WaylayService):
    """REST client for the Waylay ETL Service."""

    config_key = 'etl'
    service_key = 'etl'
    default_root_url = 'https://etl.waylay.io'
    resource_definitions = {
        'etl_import': ImportResource,
    }

    etl_import: ImportResource
