"""Test timeseries specification parser."""

import pytest


from waylay.service.timeseries.parser.model import (
    try_parse_float,
    parse_float,
    try_parse_int,
    try_parse_bool,
    parse_int,
    fromisoformat,
    SeriesSettings,
    Metric,
)

from waylay.service.timeseries.parser.etlfile import SeriesCursor, list_resources


VALUE_PARSER_TEST_CASES = [
    # case_name, values, expected, metric_args
    (
        'empty',
        [],
        [],
        dict()
    ),
    (
        'default',
        ['0', '1', '-3.14', '0.314e1', 'oops'],
        [0.0, 1.0, -3.14, 3.14, 'oops'],
        dict()
    ),
    (
        'try_parse_float',
        ['0', '1', '-3.14', '0.314e1', 'oops'],
        [0.0, 1.0, -3.14, 3.14, 'oops'],
        dict(value_parser=try_parse_float)
    ),
    (
        'try_parse_float',
        ['0', '1', '-3.14', '0.314e1', 'oops'],
        [0.0, 1.0, -3.14, 3.14, 'oops'],
        dict(value_parser=try_parse_float)
    ),
    *[
        (
            f'parse_float{value_type}',
            ['0', '1', '-3.14', '0.314e1', 'oops'],
            [0.0, 1.0, -3.14, 3.14, None],
            dict(
                value_parser=constructor,
                value_type=value_type
            )
        ) for constructor, value_type in [
            (parse_float, None),
            (None, 'float'),
            (None, 'double'),
            (parse_float, 'anything')
        ]
    ],
    (
        'try_parse_int',
        ['0', '1', '-3.14', '0.314e1', 'oops'],
        [0, 1, -3, 3, 'oops'],
        dict(value_parser=try_parse_int)
    ),
    (
        'parse_int',
        ['0', '1', '-3.14', '0.314e1', 'oops'],
        [0, 1, -3, 3, None],
        dict(value_parser=parse_int)
    ),
    (
        'bool',
        [
            '0', 'False', 'false', 'no', 'NO', 'N',
            '1', 'True', 'true', 'yes', 'YES', 'Y',
            'anything'
        ],
        [
            False, False, False, False, False, False,
            True, True, True, True, True, True,
            None
        ],
        dict(value_type='bool')
    ),
    (
        'try_bool',
        [
            '0', 'False', 'false', 'no', 'NO', 'N',
            '1', 'True', 'true', 'yes', 'YES', 'Y',
            'anything'
        ],
        [
            False, False, False, False, False, False,
            True, True, True, True, True, True,
            'anything'
        ],
        dict(value_parser=try_parse_bool)
    )
]


@pytest.fixture(params=VALUE_PARSER_TEST_CASES, ids=lambda t: t[0])
def series_cursor_values_case(request):
    """Get test cases for test_series_cursor_values."""
    return request.param


def test_series_cursor_values(series_cursor_values_case):
    """Test serialisation for a number of configuration."""
    values, expected, metric_args = series_cursor_values_case[1:]

    reader = (
        ['r1', 'm1', '2000-01-01T00:00:00Z', value]
        for value in values
    )
    metrics = [Metric(
        name='m1', **metric_args
    )]
    cursor = SeriesCursor(reader, metrics=metrics)
    values_read = [
        value
        for _, _, measures in cursor.iter_series()
        for _, value in measures
    ]
    assert values_read == expected


def assert_cursor_in_invalid_state(cursor: SeriesCursor):
    """Assert that a cursor is a state that doesn't allow to query values."""
    with pytest.raises(TypeError):
        cursor.resource
    with pytest.raises(TypeError):
        cursor.metric
    with pytest.raises(TypeError):
        cursor.timestamp
    with pytest.raises(TypeError):
        cursor.value


def test_empty_series_cursor():
    """Test a cursor on a empty dataset."""
    emtpy_reader = iter([])
    closed = [False]

    def on_close():
        closed[0] = True
    cursor = SeriesCursor(emtpy_reader, on_close=on_close)
    with pytest.raises(AssertionError):
        cursor.next_row()
    assert not cursor.next_series()
    assert not cursor.next_row()
    assert not cursor.next_row()

    # this next series comes too early, and skips the records
    # of the previous series
    cursor.next_series()
    assert not cursor.next_row()
    assert not cursor.next_row()

    assert_cursor_in_invalid_state(cursor)
    assert closed[0]


def test_two_series_cursor():
    """Test a curstor a a data set with two series and two observations."""
    reader = iter([
        ['resource', 'metric', 'timestamp', 'value'],
        ['r1', 'm1', '2000-01-01T00:00:00Z', '0'],
        ['r1', 'm2', '2000-01-01T00:00:00Z', '0']
    ])
    cursor = SeriesCursor(reader)
    assert_cursor_in_invalid_state(cursor)
    assert cursor.next_series()
    assert cursor.resource == 'r1'
    assert cursor.metric == 'm1'
    with pytest.raises(TypeError):
        cursor.timestamp
    with pytest.raises(TypeError):
        cursor.value
    assert cursor.next_row()
    assert cursor.resource == 'r1'
    assert cursor.metric == 'm1'
    assert cursor.timestamp == fromisoformat('2000-01-01T00:00:00+00:00')
    assert cursor.value == 0
    assert not cursor.next_row()
    assert cursor.next_series()
    assert cursor.next_row()
    assert cursor.resource == 'r1'
    assert cursor.metric == 'm2'
    assert cursor.timestamp == fromisoformat('2000-01-01T00:00:00+00:00')
    assert cursor.value == 0
    assert not cursor.next_series()
    assert not cursor.next_row()
    assert_cursor_in_invalid_state(cursor)


def test_two_series_cursor_iterator():
    """Test a curstor a a data set with two series and four observations."""
    reader = iter([
        ['resource', 'metric', 'timestamp', 'value'],
        ['r1', 'm1', '2000-01-01T00:00:00Z', '0'],
        ['r1', 'm1', '2000-01-01T01:00:00Z', '1'],
        ['r1', 'm2', '2000-01-01T00:00:00Z', '0'],
        ['r1', 'm2', '2000-01-01T01:00:00Z', '1'],
    ])
    result = list(
        (resource, metric, list(measures))
        for resource, metric, measures in SeriesCursor(reader).iter_series()
    )
    ts_0 = fromisoformat('2000-01-01T00:00:00+00:00')
    ts_1 = fromisoformat('2000-01-01T01:00:00+00:00')
    assert result == [
        ('r1', 'm1', [(ts_0, 0), (ts_1, 1)]),
        ('r1', 'm2', [(ts_0, 0), (ts_1, 1)]),
    ]


def test_iter_resources():
    """Test the listing of resource metrics."""
    reader = iter([
        ['resource', 'metric', 'timestamp', 'value'],
        ['r1', 'm1', '2000-01-01T00:00:00Z', '0'],
        ['r1', 'm1', '2000-01-01T01:00:00Z', '0'],
        ['r1', 'm2', '2000-01-01T00:00:00Z', '0'],
        ['r1', 'm2', '2000-01-01T01:00:00Z', '1'],
        ['r2', 'm1', '2000-01-01T01:00:00Z', '1'],
    ])

    resource_meta_list = list(
        (r.id, [m.name for m in r.metrics])
        for r in list_resources(
            SeriesSettings(), SeriesCursor(reader).iter_series()
        )
    )
    assert resource_meta_list == [
        ('r1', ['m1', 'm2']),
        ('r2', ['m1'])
    ]


def test_two_series_cursor_iterator_read_out_of_order():
    """Test failure in case series are not iterated in order."""
    reader = iter([
        ['resource', 'metric', 'timestamp', 'value'],
        ['r1', 'm1', '2000-01-01T00:00:00Z', '0'],
        ['r1', 'm1', '2000-01-01T01:00:00Z', '1'],
        ['r1', 'm2', '2000-01-01T00:00:00Z', '0']
    ])

    # this construct will skip the read out of series
    assert [('r1', 'm1'), ('r1', 'm2')] == list(
        (resource, metric)
        for resource, metric, _ in SeriesCursor(reader).iter_series()
    )
