"""Conversion from CSV to elt export format."""

from typing import (
    Union, Sequence, Iterator, Iterable,
    Optional, Tuple,
    cast
)
from dataclasses import replace
import os
import io
import csv
import gzip
from contextlib import contextmanager

from tqdm import tqdm

from .model import (
    SeriesInput,
    SeriesSettings,
    SeriesIterator,
    MeasurementIterator,
    Metric,
    CSVReader,
    PathLike,
    METRIC_PREFIX,
    METRIC_PREFIX_LENGTH,
    ETL_IMPORT_COLUMN_NAMES,
    RESOURCE_COLUMN,
    METRIC_COLUMN,
    VALUE_COLUMN,
    ParserRequestError,
    default_create_timestamp,
    TIMESTAMP_COLUMN_NAMES,
)


def prepare_settings_csv(
    input_data: SeriesInput,
    settings: SeriesSettings,
) -> SeriesSettings:
    """Validate and update the input settings by extracting metadata from a csv header."""
    with open_csv(input_data) as csv_data:
        header = next(csv_data)

        settings = _prepare_csvheader_timestamp(header, settings)

        settings = _prepare_csvheader_resource_metric(header, settings)

        if settings.value_column or all(column in header for column in ETL_IMPORT_COLUMN_NAMES):
            # single column contains values, metric must be provided fixed or as other column.
            settings = _prepare_csvheader_value_column(header, settings)
        else:
            # series specified in seperate columns
            settings = _prepare_csvheader_series_column(header, settings)

    return settings


def _prepare_csvheader_timestamp(header: Sequence[str], settings: SeriesSettings) -> SeriesSettings:
    # time column handling
    if settings.timestamp_column:
        if settings.timestamp_column not in header:
            raise ParserRequestError(
                f'Timestamp column `{settings.timestamp_column}` not in csv header.'
            )
    elif settings.timestamp_first and settings.timestamp_interval:
        raise NotImplementedError('timestamp_first timestamp_interval setting not supported')
    else:
        for timestamp_column in TIMESTAMP_COLUMN_NAMES:
            if timestamp_column in header:
                settings = replace(settings, timestamp_column=timestamp_column)
                break
        if not settings.timestamp_column:
            raise ParserRequestError(
                f'No timestamp column found in `{header}`'
            )

    # default timestamp value constructor
    if settings.timestamp_column:
        timestamp_constructor = settings.timestamp_constructor or default_create_timestamp
        if settings.timestamp_timezone:
            if settings.timestamp_constructor:
                raise ParserRequestError(
                    'Cannot specify both `timestamp_constructor` and `timestamp_timezone`.'
                )
            timezone = settings.timestamp_timezone

            def timestamp_constructor_localized(ts):
                return default_create_timestamp(ts).tz_localize(timezone)
            timestamp_constructor = timestamp_constructor_localized
            settings = replace(
                settings,
                timestamp_timezone=None
            )

        if settings.timestamp_offset:
            offset = settings.timestamp_offset
            original_timestamp_constructor = timestamp_constructor

            def timestamp_constructor_offset(ts):
                return original_timestamp_constructor(ts) + offset

            timestamp_constructor = timestamp_constructor_offset

        settings = replace(
            settings,
            timestamp_constructor=timestamp_constructor
        )
    return settings


def _prepare_csvheader_resource_metric(header: Sequence[str], settings: SeriesSettings) -> SeriesSettings:
    if not settings.resource or settings.resource_column:
        settings = replace(settings, resource_column=settings.resource_column or RESOURCE_COLUMN)
        if settings.resource_column not in header:
            raise ParserRequestError(
                f'No valid resource or resource key provided: `{settings.resource_column}`'
            )
    if settings.metric_column:
        if settings.metric_column not in header:
            raise ParserRequestError(
                f'Invalid metric key provided: `{settings.metric_column}`'
            )
    return settings


def _prepare_csvheader_value_column(header: Sequence[str], settings: SeriesSettings) -> SeriesSettings:
    if not settings.value_column:
        settings = replace(settings, value_column=VALUE_COLUMN)
    if settings.value_column not in header:
        raise ParserRequestError(
            f'Value column `{settings.value_column}` not in csv header.'
        )
    if not settings.metric and not settings.metric_column:
        if METRIC_COLUMN in header:
            settings = replace(settings, metric_column=METRIC_COLUMN)
        else:
            raise ParserRequestError(
                f'No valid metric or metric key provided for values in `{settings.value_column}` column.'
            )
    return settings


def _prepare_csvheader_series_column(header: Sequence[str], settings: SeriesSettings) -> SeriesSettings:
    specified_metrics = list(settings.iter_metrics())
    if not specified_metrics:
        specified_metrics = [
            Metric(name=column)
            for column in header
            if column != settings.timestamp_column
            if column != settings.resource_column
        ]

    specified_metrics = [
        metric_spec
        for metric_spec in specified_metrics
        if metric_spec.key_or_name in header
    ]
    if not specified_metrics:
        raise ParserRequestError(
            f'None of the specified metrics `{settings.metrics}` found in the csv header.'
        )
    return replace(settings, metrics=specified_metrics)


def iter_timeseries_csv(
    series_input: SeriesInput,
    settings: SeriesSettings,
    progress: bool = False
) -> SeriesIterator:
    """Create a SeriesIterator from the given csv input and settings.

    This reads the csv input at least once for each series.
    """
    settings = prepare_settings_csv(series_input, settings)
    resource_metric_keys = _resource_metric_keys_csv(series_input, settings)
    if progress:
        with tqdm(total=len(resource_metric_keys), unit_scale=True, unit_divisor=1, unit="series") as tqdm_progress:
            for resource_key, metric_key in resource_metric_keys:
                yield _get_timeseries_csv(series_input, settings, resource_key, metric_key)
                tqdm_progress.update(1)
    else:
        for resource_key, metric_key in resource_metric_keys:
            yield _get_timeseries_csv(series_input, settings, resource_key, metric_key)


def _get_timeseries_csv(
    series_input: SeriesInput,
    settings: SeriesSettings,
    resource_key: Optional[str],
    metric_key: str
) -> Tuple[str, str, MeasurementIterator]:
    resource = settings.resource_by_key(resource_key)
    assert resource
    metric = settings.metric_by_key(metric_key)
    assert metric

    if settings.value_column:
        # fixed value column
        return (resource, metric, _iter_timeseries_csv_one_series(
            series_input,
            settings,
            value_column=settings.value_column,
            resource_key_filter=resource_key,
            metric_key_filter=metric_key
        ))

    # fixed column: each one is a series
    return (resource, metric, _iter_timeseries_csv_one_series(
        series_input,
        settings,
        value_column=metric_key,
        resource_key_filter=resource_key,
    ))


@contextmanager
def open_csv(series_input: SeriesInput, **csv_format_args) -> Iterator[CSVReader]:
    """Open the CSV file specified by this input."""
    if isinstance(series_input, (str, os.PathLike)):
        if str(series_input).endswith('.gz'):
            yield from _open_csv_gz_file(series_input, **csv_format_args)

        else:
            yield from _open_csv_file(series_input, **csv_format_args)

    elif isinstance(series_input, io.TextIOBase):
        yield from _reset_and_open_csv_text_stream(series_input, **csv_format_args)

    elif isinstance(series_input, Iterable):
        yield from _open_csv_iterable(series_input, **csv_format_args)


def _open_csv_gz_file(series_input: PathLike, **csv_format_args) -> Iterator[CSVReader]:
    with gzip.open(series_input, 'rt') as csv_file:
        yield csv.reader(cast(io.TextIOBase, csv_file), **csv_format_args)


def _open_csv_file(series_input: PathLike, **csv_format_args) -> Iterator[CSVReader]:
    with open(series_input, 'rt') as csv_file:
        yield csv.reader(csv_file, **csv_format_args)


def _reset_and_open_csv_text_stream(series_input: io.TextIOBase, **csv_format_args) -> Iterator[CSVReader]:
    series_input.seek(0)
    yield csv.reader(series_input, **csv_format_args)


def _open_csv_iterable(
    series_input: Union[Iterable[str], Iterable[Sequence[str]]], **csv_format_args
) -> Iterator[CSVReader]:
    # inspect first item of iterable
    first_line = next(iter(series_input))
    if isinstance(first_line, str):
        # Iterable of strings, treat as unparsed csv data
        yield csv.reader(
            iter(cast(Iterable[str], series_input)),
            **csv_format_args
        )
    elif isinstance(first_line, Sequence):
        # Iterable of lists, treat as parsed csv data
        yield iter(cast(Iterable[Sequence[str]], series_input))
    else:
        raise ParserRequestError(
            f'Cannot read first line of a csv input:\n{first_line}'
        )
    return


def _resource_metric_keys_csv(
    series_input: SeriesInput,
    settings: SeriesSettings,
) -> Sequence[Tuple[Optional[str], str]]:
    fixed_metric_keys = [
        metric_spec.key_or_name for metric_spec in settings.iter_metrics()
    ]
    fixed_resource_keys = [
        resource_spec.key_or_id for resource_spec in settings.iter_resources()
    ]
    if not settings.resource_column and not settings.metric_column:
        assert settings.resource
        resource_key = settings.key_by_resource(settings.resource)
        assert resource_key
        return [
            (resource_key, metric_key) for metric_key in fixed_metric_keys
        ]

    # use an ordered dict rather than a set to retain insertion order
    resource_metric_keys_set = dict(
        (item, True)
        for item in _iter_resource_metric_keys_csv(series_input, settings)
    )
    return [
        (resource_key, metric_key)
        # (resource_key , metric_key_val) as defined in the data set
        for resource_key, metric_key_val in resource_metric_keys_set.keys()
        # if metric_key_val is not defined in data itself,
        # use the fixed metric keys (from column headers, or as specified by user)
        for metric_key in (
            [metric_key_val] if metric_key_val else fixed_metric_keys
        )
        # filter the metric_key (from data) if a filtering was given
        if not fixed_metric_keys or _remove_prefix(metric_key) in fixed_metric_keys
        # filter the resource_key (from data) if a filtering was given
        if not resource_key or not fixed_resource_keys or resource_key in fixed_resource_keys
    ]


def _remove_prefix(metric_key: str) -> str:
    if metric_key.startswith(METRIC_PREFIX):
        return metric_key[METRIC_PREFIX_LENGTH:]
    return metric_key


def _iter_resource_metric_keys_csv(
    series_input: SeriesInput,
    settings: SeriesSettings,
) -> Iterator[Tuple[Optional[str], Optional[str]]]:
    # either the resource or metric is specified as a column,
    # loop once over the complete data set to extract the combinations.
    # A None in the resulting tuple indicates that the
    # resource or metric is not defined as data, but
    # as default or row header.

    with open_csv(series_input) as csv_iter:
        header = next(csv_iter)
        resource_idx = None
        if settings.resource_column:
            resource_idx = header.index(settings.resource_column)

        metric_idx = None
        if settings.metric_column:
            metric_idx = header.index(settings.metric_column)

        for item in csv_iter:
            if not item:  # ignore empty lines
                continue
            yield (
                item[resource_idx] if resource_idx is not None else None,
                item[metric_idx] if metric_idx is not None else None
            )


def _iter_timeseries_csv_one_series(
    series_input: SeriesInput,
    settings: SeriesSettings,
    value_column: str,
    resource_key_filter: Optional[str] = None,
    metric_key_filter: Optional[str] = None,
) -> MeasurementIterator:
    with open_csv(series_input) as csv_iter:
        # inspect header
        header = next(csv_iter)
        timestamp_idx = header.index(settings.timestamp_column)
        value_idx = header.index(value_column)
        create_timestamp = settings.timestamp_constructor
        assert create_timestamp

        # Create yield loops (avoid unnessesary checks in tight loops).
        # This is a single loop that is unrolled into four cases,
        # to minimize the number of condition checks within the loop.
        resource_idx = None
        metric_idx = None
        if resource_key_filter and settings.resource_column:
            resource_idx = header.index(settings.resource_column)
        if metric_key_filter and settings.metric_column:
            metric_idx = header.index(settings.metric_column)

        if resource_idx is not None and metric_idx is not None:
            # Case 1: filtering on resource AND metric columns
            for item in csv_iter:
                if (
                    item
                    and item[metric_idx] == metric_key_filter
                    and item[resource_idx] == resource_key_filter
                ):
                    yield (create_timestamp(item[timestamp_idx]), item[value_idx])
            return

        if resource_idx is not None:
            # Case 2: filtering on resource column only
            for item in csv_iter:
                if item and item[resource_idx] == resource_key_filter:
                    yield (create_timestamp(item[timestamp_idx]), item[value_idx])
            return

        if metric_idx is not None:
            # Case 3: filtering on metric column only
            for item in csv_iter:
                if item and item[metric_idx] == metric_key_filter:
                    yield (create_timestamp(item[timestamp_idx]), item[value_idx])
            return

        # Case 4: no filtering (each row contains data for the series)
        for item in csv_iter:
            if item:
                yield (create_timestamp(item[timestamp_idx]), item[value_idx])
        return
