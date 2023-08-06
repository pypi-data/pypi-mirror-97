"""Test timeseries specification parser."""

import io
import gzip

import pandas as pd
import pytest

from waylay.service.timeseries.parser import (
    prepare_etl_import,
    create_etl_import,
    ETLFile,
    fromisoformat,
    ParserRequestError,
    Resource, Metric
)

from timeseries_parser_fixtures import (
    SERIES_LENGTH,
    assert_import_has_timeseries,
    temp_dir
)


def test_csv_simple(temp_dir):
    """Test parsing of a simple CSV input."""
    # create csv file
    csv_input_file_name = f'{temp_dir}/input.csv'
    pd.DataFrame(
        list((i, i) for i in range(SERIES_LENGTH)),
        index=pd.DatetimeIndex([f'1970-01-01T0{t}:00:00+00:00' for t in range(SERIES_LENGTH)], name='timestamp'),
        columns=['test_metric_1', 'test_metric_2'],
    ).to_csv(csv_input_file_name)

    # as csv file
    etl_import = prepare_etl_import(
        csv_input_file_name, resource='test_resource',
        import_file=ETLFile(directory=temp_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import)

    # as gzipped csv file
    csv_input_file_name_gzip = csv_input_file_name+'.gz'
    with open(csv_input_file_name, 'rt') as csv_in:
        with gzip.open(csv_input_file_name_gzip, 'wt') as csv_out:
            for line in csv_in:
                csv_out.write(line)
    etl_import = prepare_etl_import(
        csv_input_file_name_gzip, resource='test_resource',
        import_file=ETLFile(prefix='gzipped', directory=temp_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import)

    # as text stream
    with open(csv_input_file_name, 'rt') as csv_io:
        etl_import = prepare_etl_import(
            csv_io, resource='test_resource',
            import_file=ETLFile(prefix='from-stream', directory=temp_dir)
        )
        etl_import = create_etl_import(etl_import)
        assert_import_has_timeseries(etl_import)

    # as parsed string csv iterable:
    parsed_lines = [
        ('timestamp', 'test_metric_1', 'test_metric_2'),
        ('1970-01-01 00:00:00+00:00', '0', '0'),
        ('1970-01-01 01:00:00+00:00', '1', '1'),
        ('1970-01-01 02:00:00+00:00', '2', '2')
    ]
    etl_import = prepare_etl_import(
        parsed_lines, resource='test_resource',
        import_file=ETLFile(prefix='from-parsed', directory=temp_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import)

    # as parsed values csv iterable:
    parsed_lines = [
        ('timestamp', 'test_metric_1', 'test_metric_2'),
        (fromisoformat('1970-01-01T00:00:00+00:00'), 0, 0),
        (pd.Timestamp('1970-01-01T01:00:00+00:00'), 1, 1),
        ('1970-01-01T02:00:00+00:00', 2, 2.0)
    ]
    etl_import = prepare_etl_import(
        parsed_lines, resource='test_resource',
        import_file=ETLFile(prefix='from-parsed-values', directory=temp_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import)

    # as unparsed string iterable:
    unparsed_lines = [
        'timestamp,test_metric_1,test_metric_2',
        '1970-01-01 00:00:00+00:00,0,0',
        '1970-01-01 01:00:00+00:00,1,1',
        '1970-01-01 02:00:00+00:00,2,2'
    ]
    etl_import = prepare_etl_import(
        unparsed_lines, resource='test_resource',
        import_file=ETLFile(prefix='from-unparsed', directory=temp_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import)


def test_csv_import_wrong_iterable(temp_dir):
    """Test failure with interable of numbers."""
    with pytest.raises(ParserRequestError) as exc_info:
        prepare_etl_import(
            list(range(10)),
            resource='test_resource',
            import_file=ETLFile(prefix='wrong-input', directory=temp_dir)
        )
    assert 'Cannot read first line' in format(exc_info.value)


CSV_IMPORT_TEST_CASES = [
    ('multi_column', dict(resource='test_resource'), (
        "timestamp,test_metric_1,test_metric_2\n"
        "1970-01-01 00:00:00+00:00,0,0\n"
        "1970-01-01 01:00:00+00:00,1,1\n"
        "1970-01-01 02:00:00+00:00,2,2\n"
    )),
    ('value_column', dict(resource='test_resource', value_column='value'), (
        "timestamp,metric,value\n"
        "1970-01-01 00:00:00+00:00,test_metric_1,0\n"
        "1970-01-01 00:00:00+00:00,test_metric_2,0\n"
        "1970-01-01 01:00:00+00:00,test_metric_1,1\n"
        "1970-01-01 01:00:00+00:00,test_metric_2,1\n"
        "1970-01-01 02:00:00+00:00,test_metric_1,2\n"
        "1970-01-01 02:00:00+00:00,test_metric_2,2\n"
    )),
    ('resource_column', dict(timestamp_column='t', resource_column='r', metric_column='m', value_column='v'), (
        "r,t,m,v\n"
        "test_resource,1970-01-01T00:00:00+00:00,test_metric_1,0\n"
        "test_resource,1970-01-01T00:00:00+00:00,test_metric_2,0\n"
        "test_resource,1970-01-01T01:00:00+00:00,test_metric_1,1\n"
        "test_resource,1970-01-01T01:00:00+00:00,test_metric_2,1\n"
        "test_resource,1970-01-01T02:00:00+00:00,test_metric_1,2\n"
        "test_resource,1970-01-01T02:00:00+00:00,test_metric_2,2\n"
    )),
    ('resource_columns', dict(timestamp_column='t', resource_column='r'), (
        "r,t,test_metric_1,test_metric_2\n"
        "test_resource,1970-01-01 00:00:00+00:00,0,0\n"
        "test_resource,1970-01-01 01:00:00+00:00,1,1\n"
        "test_resource,1970-01-01 02:00:00+00:00,2,2\n"
    )),
    ('export_format', dict(), (
        "resource,metric,timestamp,value\n"
        "test_resource,waylay.resourcemessage.metric.test_metric_1,1970-01-01T00:00:00.000Z,0\n"
        "test_resource,waylay.resourcemessage.metric.test_metric_1,1970-01-01T01:00:00.000Z,1\n"
        "test_resource,waylay.resourcemessage.metric.test_metric_1,1970-01-01T02:00:00.000Z,2\n"
        "test_resource,waylay.resourcemessage.metric.test_metric_2,1970-01-01T00:00:00.000Z,0\n"
        "test_resource,waylay.resourcemessage.metric.test_metric_2,1970-01-01T01:00:00.000Z,1\n"
        "test_resource,waylay.resourcemessage.metric.test_metric_2,1970-01-01T02:00:00.000Z,2\n"
    )),
    (
        'export_format filtered',
        dict(
            resources=['test_resource'],
            metrics=['test_metric_1', 'test_metric_2']
        ), (
            "resource,metric,timestamp,value\n"
            "test_resource_0,waylay.resourcemessage.metric.test_metric_1,1970-01-01T00:00:00.000Z,0\n"
            "test_resource_0,waylay.resourcemessage.metric.test_metric_2,1970-01-01T00:00:00.000Z,0\n"
            "test_resource_0,waylay.resourcemessage.metric.test_metric_3,1970-01-01T00:00:00.000Z,0\n"
            "test_resource,waylay.resourcemessage.metric.test_metric_1,1970-01-01T00:00:00.000Z,0\n"
            "test_resource,waylay.resourcemessage.metric.test_metric_1,1970-01-01T01:00:00.000Z,1\n"
            "test_resource,waylay.resourcemessage.metric.test_metric_1,1970-01-01T02:00:00.000Z,2\n"
            "test_resource,waylay.resourcemessage.metric.test_metric_2,1970-01-01T00:00:00.000Z,0\n"
            "test_resource,waylay.resourcemessage.metric.test_metric_2,1970-01-01T01:00:00.000Z,1\n"
            "test_resource,waylay.resourcemessage.metric.test_metric_2,1970-01-01T02:00:00.000Z,2\n"
            "test_resource,waylay.resourcemessage.metric.test_metric_3,1970-01-01T00:00:00.000Z,0\n"
            "test_resource,waylay.resourcemessage.metric.test_metric_3,1970-01-01T01:00:00.000Z,1\n"
            "test_resource,waylay.resourcemessage.metric.test_metric_3,1970-01-01T02:00:00.000Z,2\n"

        )
    ),
    ('mapped resource-metric',
        dict(
            metrics=[
                Metric('test_metric_1', key='m_1'),
                Metric('test_metric_2', key='m_2')
            ],
            resources=[Resource('test_resource', key='0')]
        ),
        (
            "resource,timestamp,m_1,m_2\n"
            "0,1970-01-01 00:00:00+00:00,0,0\n"
            "0,1970-01-01 01:00:00+00:00,1,1\n"
            "0,1970-01-01 02:00:00+00:00,2,2\n"
        )
     ),
]


@pytest.fixture(params=CSV_IMPORT_TEST_CASES[-1:], ids=lambda t: t[0])
def csv_import_case(request):
    """Get test case for csv conversion."""
    return request.param


def test_csv_import(csv_import_case, temp_dir):
    """Test conversion of csv input."""
    case_name, import_args, csv_text = csv_import_case
    etl_import = prepare_etl_import(
        io.StringIO(csv_text),
        import_file=ETLFile(prefix=case_name, directory=temp_dir),
        **import_args
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import)


INPUT_SETTINGS_CSV_TEST_CASES = [
    # case name, args,  csv header,  validation error
    ['normalized_default',  {}, "resource,metric,timestamp,value+nr,m,2020-05-01,0", None],
    ['missing timestamp column',  {}, 'resource,metric,value', 'No timestamp column found'],
    [
        'wrong timestamp column',
        dict(timestamp_column='ts'),
        'timestamp,resource,metric,value', 'not in csv header'
    ],
    [
        'timestamp timezone and constructor',
        dict(timestamp_timezone='Europe/Brussels', timestamp_constructor=pd.Timestamp),
        'timestamp,resource,metric,value', 'Cannot specify both'
    ],
    [
        'timestamp timezone',
        dict(timestamp_timezone='Europe/Brussels'),
        "timestamp,resource,metric,value\n2020-05-01,r,m,0", None
    ],
    [
        'timestamp offset iso',
        dict(timestamp_offset='-P1D'),
        "timestamp,resource,metric,value\n2020-05-01,r,m,0", None
    ],
    [
        'timestamp offset invalid iso',
        dict(timestamp_offset='-PT1D'),
        "timestamp,resource,metric,value\n2020-05-01,r,m,0", 'Unable to parse duration'
    ],
    [
        'timestamp offset pandas',
        dict(timestamp_offset='-1h'),
        "timestamp,resource,metric,value\n2020-05-01,r,m,0", None
    ],
    [
        'missing resource',
        dict(),
        "timestamp,metric,value\n2020-05-01,m,0", 'resource or resource key'
    ],
    [
        'wrong resource key',
        dict(resource_column='abc'),
        "timestamp,metric,value\n2020-05-01,m,0", 'resource or resource key'
    ],
    [
        'wrong metric key',
        dict(resource='r', metric_column='abc'),
        "timestamp,value\n2020-05-01,0", 'Invalid metric key'
    ],
    [
        'wrong value key',
        dict(resource='r', value_column='abc'),
        "timestamp,value\n2020-05-01,0", 'not in csv header'
    ],
    [
        'no metric or metric key',
        dict(resource='r', value_column='value'),
        "timestamp,value\n2020-05-01,0", 'No valid metric'
    ],
    [
        'filter metrics',
        dict(resource='r', metric_column='m', value_column='v', metrics=['m1']),
        "timestamp,m,v\n2020-05-01,m1,0", None
    ],
    [
        'empty filter metrics',
        dict(resource='r', metric_column='m', value_column='v', metrics=['m1']),
        "timestamp,m,v\n2020-05-01,m2,0", None
    ],
    [
        'ignore empty lines',
        dict(resource='r', metric_column='m', value_column='v', metrics=['m1']),
        "timestamp,m,v\n\n2020-05-01,m1,0\n\n\n", None
    ],
    [
        'wrong filter on metric columns',
        dict(resource='r', metrics=['m1']),
        "timestamp,m2\n\n2020-05-01,0\n\n\n", 'found in the csv header'
    ],
    [
        'resource filter',
        dict(
            resource_column='resource',
            resources=['r1'],
            metrics=['temperature']
        ),
        (
            "resource,timestamp,temperature,humidity\n"
            "r1,2021-03-01T00:00Z,-1,203\n"
            "r2,2021-03-01T03:00Z,-2,201\n"
            "r1,2021-03-01T06:00Z,3,221\n"
            "r2,2021-03-01T09:00Z,10,223\n"
            "r1,2021-03-01T12:00Z,15,243\n"
            "r2,2021-03-01T15:00Z,21,183\n"
            "r1,2021-03-01T18:00Z,14,203\n"
            "r2,2021-03-01T21:00Z,8,200\n"
        ),
        None
    ],
    [
        'etl export format',
        dict(metrics=['activeScore']),
        (
            "resource,metric,timestamp,value\n"
            "fitbitsimulator.00574,waylay.resourcemessage.metric.activeScore,2021-02-21T14:27:02.391Z,-1\n"
            "fitbitsimulator.00574,waylay.resourcemessage.metric.activeScore,2021-02-21T14:48:34.300Z,2\n"
            "fitbitsimulator.00574,waylay.resourcemessage.metric.activeScore,2021-02-21T14:49:10.541Z,2\n"
        ),
        None
    ]
]


@pytest.fixture(params=INPUT_SETTINGS_CSV_TEST_CASES[:], ids=lambda t: t[0])
def prepare_settings_csv_case(request):
    """Parametrize csv input test cases."""
    return request.param


def test_prepare_settings_csv(prepare_settings_csv_case, temp_dir):
    """Test csv input specifications."""
    case_name, import_args, csv_text, error_text = prepare_settings_csv_case

    try:
        etl_import = prepare_etl_import(
            io.StringIO(csv_text+"\n"),
            import_file=ETLFile(prefix=case_name, directory=temp_dir),
            **import_args
        )
        create_etl_import(etl_import)
        if error_text:
            raise AssertionError(f'expected a failure: {error_text}')

    except ParserRequestError as e:
        if error_text:
            assert error_text in format(e)
        else:
            raise e
