"""Utilities to parse and render ETL timeseries files."""
from typing import (
    Optional, Union, Tuple, Any, Set,
    Sequence,
    List, Callable,
    Iterable,
    Iterator,
    ContextManager,
    cast
)
import gzip
import csv
import sys
import io
import os
from pathlib import Path
from datetime import datetime
from dataclasses import replace
from contextlib import contextmanager

import pandas as pd

from waylay.exceptions import RequestError

from .model import (
    Metric,
    Resource,
    SeriesSettings,
    ETLFile,
    WaylayETLSeriesImport,

    SeriesInput,

    MeasurementValue,
    Measurement,
    MeasurementIterator,

    SeriesIterator,
    ETL_IMPORT_COLUMN_NAMES,

    render_timestamp,
    try_parse_float,
    fromisoformat,
    default_create_timestamp,
    ParserRequestError,
)
from .import_csv import (
    prepare_settings_csv,
    iter_timeseries_csv
)
from .import_dataframe import (
    prepare_settings_dataframe,
    iter_timeseries_dataframe
)
from .etlfile import (
    read_etl_import_as_stream,
    read_etl_import,
    dataframe_from_iterator,
    list_resources,
)


def iter_timeseries(
    input_data: SeriesInput,
    settings: SeriesSettings,
    progress: bool = False
) -> SeriesIterator:
    """Create a SeriesInterator for the given input source and settings."""
    if isinstance(input_data, pd.DataFrame):
        return iter_timeseries_dataframe(input_data, settings, progress)
    else:
        return iter_timeseries_csv(input_data, settings, progress)


def prepare_etl_import(
    series_input: SeriesInput,
    import_file: Optional[ETLFile] = None,
    settings: Optional[SeriesSettings] = None,
    **settings_args: Any
) -> WaylayETLSeriesImport:
    """Update the mapping settings by extracting metadata from an input source."""
    import_file = import_file or ETLFile()
    settings = settings or SeriesSettings()
    if settings_args:
        settings = replace(settings, **settings_args)

    # input settings validation
    etl_import = WaylayETLSeriesImport(
        series_input=series_input,
        settings=settings,
        import_file=import_file
    )

    # input series validation
    if isinstance(series_input, pd.DataFrame):
        settings = prepare_settings_dataframe(series_input, settings)
        etl_import = replace(etl_import, settings=settings)
    else:
        settings = prepare_settings_csv(series_input, settings)
        etl_import = replace(etl_import, settings=settings)
    return etl_import


def create_etl_import(
    etl_import: WaylayETLSeriesImport,
    progress: bool = True
) -> WaylayETLSeriesImport:
    """Create an ETL import file from the given input."""
    file_path = etl_import.import_file.path
    if file_path.exists():
        raise RequestError(
            f'The file {file_path} already exists. '
            'Please remove or specify another etl-import file name.'
        )

    timeseries_data = iter_timeseries(etl_import.series_input, etl_import.settings, progress=progress)
    with gzip.open(file_path, 'wt') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(ETL_IMPORT_COLUMN_NAMES)
        for resource, metric, measurements in timeseries_data:
            for timestamp, value in measurements:
                writer.writerow([
                    resource,
                    metric,
                    render_timestamp(timestamp),
                    value
                ])
    return etl_import
