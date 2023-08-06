"""Test timeseries specification parser."""

from datetime import timedelta
from dataclasses import asdict

import pandas as pd
import numpy
import pytest

from waylay.service.timeseries.parser import (
    prepare_etl_import,
    iter_timeseries_dataframe,
    iter_timeseries,
    dataframe_from_iterator,
    create_etl_import,
    read_etl_import,
    ETLFile,
    SeriesSettings,
    ParserRequestError,
)

from timeseries_parser_fixtures import (
    SERIES_LENGTH,
    assert_import_has_timeseries,
    assert_timeseries_data_equal,
    temp_dir,
    default_timeseries_data
)


def test_pandas_simple(temp_dir):
    """Test parsing of a pandas dataframe."""
    input_data = pd.DataFrame(
        list((i, i) for i in range(SERIES_LENGTH)),
        index=pd.DatetimeIndex([f'1970-01-01T0{t}:00:00+00:00' for t in range(SERIES_LENGTH)]),
        columns=['test_metric_1', 'test_metric_2'],
    )
    etl_import = prepare_etl_import(
        input_data, resource='test_resource',
        import_file=ETLFile(directory=temp_dir)
    )

    timeseries_it = iter_timeseries_dataframe(input_data, etl_import.settings)
    assert_timeseries_data_equal(timeseries_it, default_timeseries_data())

    etl_import = create_etl_import(etl_import)

    assert_import_has_timeseries(etl_import)

    with read_etl_import(etl_import) as timeseries_from_zip:
        df_from_zip = dataframe_from_iterator(timeseries_from_zip)
        assert numpy.array_equal(df_from_zip.values, input_data.values)
        assert numpy.array_equal(df_from_zip.index.values, input_data.index.values)


@pytest.fixture(params=[
    ('metric', 'xx', ''),
    ('name', 'xx', ''),
    ('other', 'xx', 'xx-')
], ids=lambda t: t[0])
def metric_attribute_case(request):
    """Generate cases for the multicolumn test."""
    return request.param


def test_pandas_multicolumn(metric_attribute_case):
    """Test dataframe iterator."""
    metric_attribute_key, info, prefix = metric_attribute_case
    input = pd.DataFrame(
        list((i, i) for i in range(SERIES_LENGTH)),
        index=pd.DatetimeIndex([f'1970-01-01T0{t}:00:00+00:00' for t in range(SERIES_LENGTH)]),
        columns=pd.MultiIndex.from_tuples(
            [(info, 'test_metric_1',), (info, 'test_metric_2',)],
            names=['info', metric_attribute_key]
        )
    )
    settings = SeriesSettings(resource='test_resource')

    timeseries_it = iter_timeseries_dataframe(input, settings)
    assert_timeseries_data_equal(
        timeseries_it,
        default_timeseries_data(metric_prefix=prefix)
    )


EMPTY_DATAFRAME = pd.DataFrame()
INPUT_SETTINGS_DATAFRAME_TEST_CASES = [
    # case,  dataframe, input settings, expected settings, error text fragment
    ['empty',  EMPTY_DATAFRAME, {}, None, None, 'index of type'],
    ['no index',  EMPTY_DATAFRAME, dict(resource='R'), None, None, 'index of type'],
    ['no resource', pd.DataFrame(index=pd.DatetimeIndex([])), {}, None,  None, 'specify a resource'],

    ['resource',  pd.DataFrame(index=pd.DatetimeIndex([])), dict(resource='R'), dict(resource='R'), [], None],
    ['resourcemetric',
        pd.DataFrame(columns=['M'], index=pd.DatetimeIndex([])),
        dict(resource='R'), dict(resource='R'), [('R', 'M')], None
     ],
    [
        'resource from default level',
        pd.DataFrame(
            columns=pd.MultiIndex.from_tuples([('R', 'M')], names=('resource', 'metric')),
            index=pd.DatetimeIndex([])
        ),
        {},
        {},
        [('R', 'M')],
        None
    ],
    [
        'resource from resource_column level',
        pd.DataFrame(
            columns=pd.MultiIndex.from_tuples([('R', 'M')], names=('res', 'metric')),
            index=pd.DatetimeIndex([])
        ),
        dict(resource_column='res'),
        {},
        [('R', 'M')],
        None
    ],
    [
        'resource from resource_column column',
        pd.DataFrame(
            columns=['res', 'metric', 'value'],
            index=pd.DatetimeIndex([])
        ),
        dict(resource_column='res'),
        {},
        [('R', 'M')],
        'NOT YET SUPPORTED'
    ],
    [
        'resource from resource column',
        pd.DataFrame(
            columns=['resource', 'metric', 'value'],
            index=pd.DatetimeIndex([])
        ),
        {},
        {},
        [('R', 'M')],
        'NOT YET SUPPORTED'
    ],
    [
        'wrong resource key',
        pd.DataFrame(
            columns=['resource', 'metric', 'value'],
            index=pd.DatetimeIndex([])
        ),
        dict(resource_column='res'),
        {},
        [('R', 'M')],
        'invalid `resource_column`'
    ],
    [
        'wrong resource key multiindex',
        pd.DataFrame(
            columns=pd.MultiIndex.from_tuples([('R', 'M')], names=('resource', 'metric')),
            index=pd.DatetimeIndex([])
        ),
        dict(resource_column='res'),
        {},
        [('R', 'M')],
        'invalid `resource_column`'
    ],
    [
        'no resource multiindex',
        pd.DataFrame(
            columns=pd.MultiIndex.from_tuples([('R', 'M')], names=('a', 'b')),
            index=pd.DatetimeIndex([])
        ),
        dict(),
        {},
        [('R', 'M')],
        'specify a resource'
    ],
    [
        'resource key multiindex',
        pd.DataFrame(
            columns=pd.MultiIndex.from_tuples([('M1', 'R', 'M2')], names=('a', 'b', 'c')),
            index=pd.DatetimeIndex([])
        ),
        dict(resource_column='b'),
        {},
        [('R', 'M1-M2')],
        None
    ],
    [
        'metrics by column',
        pd.DataFrame(
            columns=['a', 'b'],
            index=pd.DatetimeIndex([])
        ),
        dict(resource='R'),
        {},
        [('R', 'a'), ('R', 'b')],
        None
    ],
    [
        'metric key by column',
        pd.DataFrame(
            columns=['a', 'b'],
            index=pd.DatetimeIndex([])
        ),
        dict(resource='R', metric_column='a'),
        {},
        [],
        'NOT YET SUPPORTED'
    ],
    [
        'wrong metric key',
        pd.DataFrame(
            columns=['a', 'b'],
            index=pd.DatetimeIndex([])
        ),
        dict(resource='R', metric_column='res'),
        {},
        None,
        'invalid `metric_column`'
    ],
    [
        'metric key in multindex',
        pd.DataFrame(
            columns=pd.MultiIndex.from_tuples([('X', 'M')], names=('x', 'mtr')),
            index=pd.DatetimeIndex([])
        ),
        dict(resource='R', metric_column='mtr'),
        {},
        [('R', 'M')],
        None
    ],
    [
        'wrong metric key in multindex',
        pd.DataFrame(
            columns=pd.MultiIndex.from_tuples([('X', 'M')], names=('x', 'mtr')),
            index=pd.DatetimeIndex([])
        ),
        dict(resource='R', metric_column='rtm'),
        {},
        [],
        'invalid `metric_column`'
    ],
    [
        'timestamp column',
        pd.DataFrame(
            columns=['timestamp', 'a']
        ),
        dict(resource='R'),
        {},
        [('R', 'a')],
        None
    ],
    [
        'timestamp_column column',
        pd.DataFrame(
            columns=['ts', 'a']
        ),
        dict(resource='R', timestamp_column='ts'),
        {},
        [('R', 'a')],
        None
    ],
    [
        'wrong timestamp_column column',
        pd.DataFrame(
            columns=['ts', 'a']
        ),
        dict(resource='R', timestamp_column='tsx'),
        {},
        [('R', 'a')],
        '`timestamp_column` setting'
    ],
    [
        'timestamp interval',
        pd.DataFrame(
            columns=['a']
        ),
        dict(resource='R', timestamp_interval=timedelta(seconds=30)),
        {},
        [('R', 'a')],
        None
    ],
    [
        'value_column',
        pd.DataFrame(
            columns=['t', 'r', 'm', 'v']
        ),
        dict(
            timestamp_column='t',
            resource_column='r',
            metric_column='m',
            value_column='v'
        ),
        {},
        [],
        'NOT YET SUPPORTED'
    ],
    [
        'wrong value_column',
        pd.DataFrame(
            columns=['t', 'r', 'm', 'v']
        ),
        dict(
            timestamp_column='t',
            resource_column='r',
            metric_column='m',
            value_column='vv'
        ),
        {},
        [],
        'invalid `value_column`'
    ],
    [
        'value_column but no metric',
        pd.DataFrame(
            columns=['t', 'r', 'v']
        ),
        dict(
            timestamp_column='t',
            resource_column='r',
            value_column='v'
        ),
        {},
        [],
        '`metric_column` should be specified'
    ],
]


@pytest.fixture(params=INPUT_SETTINGS_DATAFRAME_TEST_CASES[:], ids=lambda t: t[0])
def prepare_settings_dataframe_case(request):
    """Parametrize dataframe test cases."""
    return request.param


def test_prepare_settings_dataframe(prepare_settings_dataframe_case):
    """Test parsing of dataframes for a number of input settings."""
    name, df, settings, expected_settings, expected_rv, error_text_fragment = prepare_settings_dataframe_case
    try:
        etl_import = prepare_etl_import(df, **settings)
        if expected_settings:
            for k, v in expected_settings.items():
                if v is None:
                    assert expected_settings.get(k, None) is None
                else:
                    assert k in expected_settings
                    assert expected_settings[k] == v
        if expected_rv is not None:
            assert expected_rv == list(
                (r, v)
                for rr, mm, vv in iter_timeseries_dataframe(df, etl_import.settings)
                for r, v, series in [(rr, mm, list(vv))]
            )
        if error_text_fragment:
            raise AssertionError(f'expected a ParserRequestError(...{error_text_fragment}...)')
    except ParserRequestError as e:
        if error_text_fragment:
            assert error_text_fragment in format(e)
        else:
            raise e


REFERENCE_TIMESTAMP = pd.Timestamp('2021-02-01T21:01:02+00:00')
TIMESTAMP_TEST_CASES = [
    (
        'base', pd.DataFrame(
            [[0]],
            columns=['a'],
            index=pd.DatetimeIndex([REFERENCE_TIMESTAMP])
        ), dict(resource='R'), None),
    (
        'timestamp_column', pd.DataFrame(
            [['2021-02-01T21:01:02+00:00', 0]],
            columns=['timestamp', 'a']
        ), dict(
            resource='R',
        ), None),
    (
        'timestamp_constructor', pd.DataFrame(
            [['21:01:02+00:00', 0]],
            columns=['timestamp', 'a']
        ), dict(
            resource='R',
            timestamp_constructor=lambda t: '2021-02-01T'+t
        ), None),
    (
        'timestamp_offset', pd.DataFrame(
            [['2021-02-02T21:01:02+00:00', 0]],
            columns=['timestamp', 'a']
        ), dict(
            resource='R',
            timestamp_offset=timedelta(days=-1)
        ), None),
    (
        'timestamp_first', pd.DataFrame(
            [['2099-02-02T21:01:02+00:00', 0]],
            columns=['timestamp', 'a']
        ), dict(
            resource='R',
            timestamp_first=REFERENCE_TIMESTAMP
        ), None),
    (
        'timestamp_first interval', pd.DataFrame(
            [
                [0],
                [1]
            ],
            columns=['a']
        ), dict(
            resource='R',
            timestamp_interval=timedelta(hours=1),
            timestamp_first=REFERENCE_TIMESTAMP
        ), None),
    (
        'timestamp_last', pd.DataFrame(
            [
                ['2099-02-02T21:01:02+00:00', 0],
                ['2099-02-02T22:01:02+00:00', 1]
            ],
            columns=['timestamp', 'a']
        ), dict(
            resource='R',
            timestamp_last=REFERENCE_TIMESTAMP + timedelta(hours=1)
        ), None),
    (
        'timestamp_last interval', pd.DataFrame(
            [
                [0],
                [1]
            ],
            columns=['a']
        ), dict(
            resource='R',
            timestamp_interval=timedelta(hours=1),
            timestamp_last=REFERENCE_TIMESTAMP + timedelta(hours=1)
        ), None),
    (
        'timestamp_offset conflict', pd.DataFrame(
            [['2099-02-02T21:01:02+00:00', 0]],
            columns=['timestamp', 'a']
        ), dict(
            resource='R',
            timestamp_first=REFERENCE_TIMESTAMP,
            timestamp_last=REFERENCE_TIMESTAMP
        ), 'offset the timestamps'),
    (
        'fail timestamp localtime', pd.DataFrame(
            [['2099-02-02T21:01:02', 0]],
            columns=['timestamp', 'a']
        ), dict(
            resource='R',
        ), 'UTC timestamp'),
    (
        'non GMT timestamp', pd.DataFrame(
            [['2021-02-01T22:01:02+01:00', 0]],
            columns=['timestamp', 'a']
        ), dict(
            resource='R',
        ),  None),
    (
        'timezone provided', pd.DataFrame(
            [['2021-02-01T22:01:02', 0]],
            columns=['timestamp', 'a']
        ), dict(
            resource='R',
            timestamp_timezone='Europe/Brussels'
        ),  None),
    (
        'timezone offset provided', pd.DataFrame(
            [['2021-02-01T22:01:02', 0]],
            columns=['timestamp', 'a']
        ), dict(
            resource='R',
            timestamp_timezone='UTC',
            timestamp_offset=pd.to_timedelta('-1h')
        ),  None),
]


@pytest.fixture(params=TIMESTAMP_TEST_CASES[:], ids=lambda t: t[0])
def prepare_timestamp_case(request):
    """Parametrize timestamp test cases."""
    return request.param


def test_prepare_timestamp(prepare_timestamp_case):
    """Test timestamp handling for a number of cases."""
    name, df, settings, error_text_fragment = prepare_timestamp_case
    try:
        etl_import = prepare_etl_import(df, **settings)
        _, _, series = next(iter_timeseries(df, etl_import.settings))
        assert REFERENCE_TIMESTAMP == next(series)[0]
        second_row = next(series, None)
        if second_row:
            (second_row[0] - REFERENCE_TIMESTAMP) == timedelta(hours=1)
        if error_text_fragment:
            raise AssertionError(f'expected a ParserRequestError(...{error_text_fragment}...)')
    except ParserRequestError as e:
        if error_text_fragment:
            assert error_text_fragment in format(e)
        else:
            raise e
