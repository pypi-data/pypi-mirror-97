"""ETL import tooling."""
__docformat__ = "google"

from typing import Any, Optional, List, Dict, Iterator
from enum import Enum
from dataclasses import dataclass, asdict
from contextlib import contextmanager

import pandas as pd

from waylay.service.storage import StorageService
from waylay.service.etl import ETLService
from waylay.service.api import ApiService
from waylay.service.analytics import AnalyticsService

from .parser.model import (
    SeriesInput,
    SeriesSettings,
    WaylayETLSeriesImport,
    ETLFile,
    PathLike,
    ETL_IMPORT_BUCKET,
    CSVReader,
    Resource,
)

from .parser import (
    prepare_etl_import,
    create_etl_import,
    dataframe_from_iterator,
    read_etl_import,
    read_etl_import_as_stream,
    list_resources,
)

ETL_IMPORT_TIMESERIES_FILE_SUFFIX = '-timeseries.csv.gz'
ETL_IMPORT_RESULT_FILE_SUFFIX = '.result.json'
ETL_IMPORT_SUFFIXES = [ETL_IMPORT_TIMESERIES_FILE_SUFFIX, ETL_IMPORT_RESULT_FILE_SUFFIX]


class ETLImportStatus(str, Enum):
    """The possible states of an ETL import job.

    These correspond to the subfolders of the 'etl-import' bucket (except for 'not_found').
    """

    UPLOAD = 'upload'
    BUSY = 'busy'
    FAILED = 'failed'
    IGNORED = 'ignored'
    DONE = 'done'
    NOT_FOUND = 'not_found'


ETL_IMPORT_STATUS_MESSAGE = {
    ETLImportStatus.UPLOAD:
    'The upload has not been picked up by the ETL process. '
    'Please contact support if this persists.',
    ETLImportStatus.BUSY:
    'The upload is being processed by the ETL process.',
    ETLImportStatus.FAILED:
    'The upload could not be processed by the ETL process. Pleasy try again or contact support.',
    ETLImportStatus.IGNORED:
    'The upload did not satisfy the formatting rules of an ETL import.',
    ETLImportStatus.DONE:
    'The upload has been processed by the ETL process. Please inspect the processing report.',
    ETLImportStatus.NOT_FOUND:
    'The upload could not be found on the storage server. Please try again.'

}
ETL_IMPORT_UPLOAD_PROCESS_STATUSES = [
    ETLImportStatus.BUSY,
    ETLImportStatus.FAILED,
    ETLImportStatus.DONE
]


@dataclass
class ETLImportJob:
    """Response object for the status of an etl upload.

    Reports the status of an ETL import job as executed by the ETL Server and recorded in
    the 'etl-import' storage bucket.

    Attributes:
        name: The (base) name of the ETL file as a storage object in the 'etl-import' bucket.
        message: A human readable status message.
        status: The import job status.
        storage: A link to the storage location.
        etl_import:
            The response object of the ETL Server for this job, as stored on the 'etl-import' bucket.
        last_etl_import:
            The response object of the last job handled by the ETL Server.
            Only included when inspecting the status of a specific upload ('check_import').
    """

    name: str
    message: str
    status: ETLImportStatus
    storage: Optional[str] = None
    etl_import: Optional[Dict] = None
    last_etl_import: Optional[Dict] = None

    def to_dict(self) -> Dict[str, Any]:
        """Return a dict representation."""
        return asdict(self)

    def to_dataframe(self) -> pd.DataFrame:
        """Return a dataframe representation."""
        data_dict = asdict(self)
        data_entries = [
            (('Upload', k), format(v))
            for k, v in data_dict.items()
            if k in ['name', 'message', 'status']
            if v
        ]
        if self.storage:
            data_entries.append(
                (('Upload', 'storage'), format(self.storage))
            )
        if self.etl_import:
            data_entries.extend(
                (('ETL Import Result', k), format(v))
                for k, v in self.etl_import.items()
            )
        if self.last_etl_import:
            data_entries.extend(
                (('Last ETL Import Result', k), format(v))
                for k, v in self.last_etl_import.items()
            )
        return pd.DataFrame(
            columns=[''],
            index=pd.MultiIndex.from_tuples(
                [d[0] for d in data_entries],
                names=('', '')
            ),
            data=[format(d[1]) for d in data_entries]
        )

    def to_html(self) -> str:
        """Return an HTML string representation."""
        return self.to_dataframe().to_html(escape=False)


class TimeSeriesETLTool:
    """Client tool to prepare and upload timeseries data.

    Attributes:
        storage_service:
            Storage service client used by this tool.
        etl_service:
            ETL service client used by this tool.
        temp_dir:
            Default temporary directory used for processes initiated by this tool.
    """

    def __init__(
        self,
        storage_service: StorageService,
        etl_service: ETLService,
        api_service: ApiService,
        analytics_service: AnalyticsService,
        temp_dir: Optional[PathLike] = None
    ):
        """Create the timeseries etl import tool."""
        self.storage_service = storage_service
        self.etl_service = etl_service
        self.api_service = api_service
        self.analytics_service = analytics_service
        self.temp_dir = temp_dir

    def prepare_import(
        self,
        series: SeriesInput,
        name: Optional[str] = None,
        temp_dir: Optional[PathLike] = None,
        settings: Optional[SeriesSettings] = None,
        progress: bool = True,
        **settings_args: Any
    ) -> WaylayETLSeriesImport:
        """Convert an input data set to a locally stored timeseries file.

        This created file can be ingested by the waylay system as timeseries data.
        Args:
            series: A supported CSV of pandas Dataframe input source.
            name:
                A name for the upload job, will be used in naming the ETL file.
                (default: 'import-{timestamp}')
            temp_dir:
                The local storage location to use in preparing the ETL file.
                (default: a system generated temp file with prefix 'etl-import')
            settings:
                A full specification object for the data conversion. Alternatively,
                attributes of this `SeriesSettings` object can be specified as keyword
                argument.
            progress:
                Write a progress bar for the conversion to standard output.
            **settings_args:
                Any attribute of a `SeriesSettings` object. See `settings` above.
        """
        etl_file = ETLFile(temp_dir or self.temp_dir, name)
        etl_import = prepare_etl_import(series, etl_file, settings, **settings_args)
        return create_etl_import(etl_import, progress=progress)

    def initiate_import(self, etl_import: WaylayETLSeriesImport) -> WaylayETLSeriesImport:
        """Upload a prepared timeseries file to the etl-import ingestion bucket.

        Args:
            etl_import:
                A reference object to the input source and converted etl file, as
                produced by `prepare_import`.
        """
        self.storage_service.content.put(
            etl_import.storage_bucket,
            etl_import.storage_object_name,
            from_file=etl_import.import_file.path,
            content_type='application/gzip',
        )
        return etl_import

    def list_import(
        self,
        name_filter: Optional[str] = None,
        status_filter: Optional[List[ETLImportStatus]] = None
    ) -> List[ETLImportJob]:
        """List all imports in all states on the `etl-import` bucket.

        This queries both the content of the `etl-import` bucket,
        and the current or last job held by the ETL Service.

        Args:
            name_filter:
                A query filter on the name of the etl import files to consider.
            status_filter:
                A filter on the status of the import jobs, a list of strings
                as enumerated in `ETLImportStatus`

        Returns:
            A list of 'ETLImportJob' objects that represent the processing status
            of an ETL import job.
        """
        # query storage objects in 'etl-import' bucket
        if name_filter:
            name_filter = name_filter.replace(ETL_IMPORT_TIMESERIES_FILE_SUFFIX, '')

        etl_upload_objects = [
            obj['name']
            for obj in self.storage_service.object.iter_list_all(
                ETL_IMPORT_BUCKET, '', params=dict(recursive=True, max_keys=900)
            )
            if any(
                obj['name'].startswith(f'{status}/')
                for status in ETLImportStatus
                if (not status_filter or status in status_filter)
            )
            if any(
                obj['name'].endswith(suffix)
                for suffix in ETL_IMPORT_SUFFIXES
            )
            if (name_filter is None or name_filter in obj['name'])
        ]

        response_by_key: Dict[str, ETLImportJob] = {}
        # create a ETLImportJob per timeseries upload file
        for obj_name in etl_upload_objects:
            if obj_name.endswith(ETL_IMPORT_TIMESERIES_FILE_SUFFIX):
                key = obj_name.replace(ETL_IMPORT_TIMESERIES_FILE_SUFFIX, '')
                status = obj_name.split('/')[0]
                get_url = self.storage_service.object.sign_get(ETL_IMPORT_BUCKET, obj_name)
                resp = ETLImportJob(
                    name=obj_name.split('/')[-1],
                    status=status,
                    message=ETL_IMPORT_STATUS_MESSAGE[status],
                    storage=f'<a href="{get_url}">{obj_name}</a>'
                )
                response_by_key[key] = resp

        # amend a ETLImportJob for each result file
        for obj_name in etl_upload_objects:
            if obj_name.endswith(ETL_IMPORT_RESULT_FILE_SUFFIX):
                key = obj_name.replace(ETL_IMPORT_RESULT_FILE_SUFFIX, '')
                upload_file_resp = response_by_key.get(key)
                if upload_file_resp:
                    resp_content = self.storage_service.content.get(ETL_IMPORT_BUCKET, obj_name)
                    upload_file_resp.etl_import = resp_content.json()  # type: ignore

        return list(response_by_key.values())

    def check_import(self, etl_import: WaylayETLSeriesImport) -> ETLImportJob:
        """Validate the status of an import process started by this tool.

        Args:
            etl_import:
                The object representing the converted ETL import file,
                as produced by `initiate_import`.
        Returns:
            An object representing the current status of the ETL import job.
        """
        import_listing = [
            import_status
            for import_status in self.list_import(name_filter=etl_import.import_file.name)
            if import_status.name == etl_import.import_file.name
        ]

        if not import_listing:
            return ETLImportJob(
                name=etl_import.storage_object_name,
                status=ETLImportStatus.NOT_FOUND,
                message=ETL_IMPORT_STATUS_MESSAGE[ETLImportStatus.NOT_FOUND],
                storage=None
            )
        response = import_listing[0]

        if len(import_listing) > 1:
            listing = ''.join(f'<li>{import_job.storage}</li>' for import_job in import_listing)
            response.message = response.message + (
                '<br>Multiple import jobs with identically named import files have been found:'
                f'<ul>{listing}</ul>'
                'Please provide unique names for each import file.'
            )

        # current etl import task
        current_etl_import = self.etl_service.etl_import.get()

        # only add if different from saved etl import result for current job
        if (
            not response.etl_import
            or response.etl_import.get('filename', '') != current_etl_import.get('filename')
        ):
            response.last_etl_import = current_etl_import

        # warn if current etl is not the same as selected
        if 'filename' in current_etl_import:
            current_etl_filename = current_etl_import['filename']
            if etl_import.import_file.name not in current_etl_filename:
                response.message = response.message + \
                    '<br>The ETL service is/has currently been processing another import.'

        return response

    @contextmanager
    def read_import_as_csv(self, etl_import: WaylayETLSeriesImport) -> Iterator[CSVReader]:
        """Read an etl import file as a csv stream.

        This returns a context manager that provides an iterator
        of csv rows (`Iterator[Sequence[str]]`):

            with etl_tool.read_import_as_csv(etl_import) as csv_data:
                for csv_line in csv_data:
                    print("|".join(csv_line))

        Args:
            etl_import:
                The object representing the converted ETL import file,
                as produced by `prepare_import`.

        Returns:
            A context manager providing an iterator of string records.

        """
        with read_etl_import_as_stream(etl_import) as csv_iterator:
            yield csv_iterator

    def read_import_as_dataframe(self, etl_import: WaylayETLSeriesImport) -> pd.DataFrame:
        """Read an etl import file as pandas dataframe.

        Args:
            etl_import:
                The object representing the converted ETL import file,
                as produced by `prepare_import`.

        Returns:
            A pandas Dataframe containing the import data.
            Each series is a seperate column. Column headers
            contain a `resource` and `metric` reference.
            When the input specification of the `etl_import` contains
            a `metrics` object with a `value_type` or `value_parser` attribute,
            the corresponding csv series is converted to that data type.
        """
        with read_etl_import(etl_import) as series_iterator:
            return dataframe_from_iterator(series_iterator)

    def list_import_resources(
        self,
        etl_import: WaylayETLSeriesImport
    ) -> List[Resource]:
        """List resource and metric metadata contained in an ETL import file.

        Args:
            etl_import:
                The object representing the converted ETL import file,
                as produced by `prepare_import`.

        Returns:
            A list of `Resource` metadata objects describing the
            content of the import file.
        """
        with read_etl_import(etl_import) as series_iterator:
            return list_resources(etl_import.settings, series_iterator)

    def update_resources(
        self,
        etl_import: WaylayETLSeriesImport
    ) -> List[Resource]:
        """Create or update the Waylay Resources for the timeseries in this dataset.

        Args:
            etl_import:
                The object representing the converted ETL import file,
                as produced by `prepare_import`.

        Returns:
            A list of `Resource` metadata objects describing the
            content of the import file, and for which metadata has been updated
            to the waylay system
        """
        resources = self.list_import_resources(etl_import)
        for resource in resources:
            self.api_service.resource.update(resource.id, body=resource.to_dict())
        return resources

    def update_query(
        self,
        etl_import: WaylayETLSeriesImport,
        name: Optional[str] = None,
        **query_params: Any
    ) -> Any:
        """Create or update a waylay query containing all the series defined in this import.

        The name of the import will be used as query name.
        Args:
            etl_import:
                The object representing the converted ETL import file,
                as produced by `prepare_import`.
            name:
                The name of the query. Defaults to the prefix name of
                the etl_import argument (`etl_import.import_file.prefix`).
            query_params:
                Any additional query params (like `from`, `util`, `freq`, `aggregation`, ...)
                to be used in the query

        Returns:
            The result of a `analytics.query.replace()` SDK call that
            updated or created the query with the name of the import.
        """
        query_name = name or etl_import.import_file.prefix
        resources = self.list_import_resources(etl_import)
        with self.read_import_as_csv(etl_import) as csv_lines:
            header = next(csv_lines)
            ts_idx = header.index(etl_import.settings.timestamp_column)
            first_timestamp = next(csv_lines)[ts_idx]
        query = {
            'from': first_timestamp,
            'data': [
                {
                    'resource': resource.id,
                    'metric': metric.name
                }
                for resource in resources
                for metric in resource.metrics or []
            ]
        }
        query.update(query_params)
        return self.analytics_service.query.replace(query_name, body={'query': query})
