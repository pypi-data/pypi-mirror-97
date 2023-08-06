"""Timeseries parser test utitlities."""
import tempfile
import pytest

from waylay.service.timeseries.parser import (
    MeasurementIterator,
    SeriesIterator,
    WaylayETLSeriesImport,
    read_etl_import,
    fromisoformat
)

DONE = 'done'


@pytest.fixture
def temp_dir():
    """Create (and cleanup) a temporary directory."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


def assert_timeseries_equal(timeseries_1: MeasurementIterator, timeseries_2: MeasurementIterator):
    """Assert that two measurement iterators are identical.

    Consumes the iterators.
    """
    while True:
        t_1, v_1 = next(timeseries_1, (DONE, None))
        t_2, v_2 = next(timeseries_2, (DONE, None))
        if t_1 == DONE and t_2 == DONE:
            return
        assert t_1 == t_2
        assert v_1 == v_2


def assert_timeseries_data_equal(timeseries_1: SeriesIterator, timeseries_2: SeriesIterator):
    """Assert that two timeseries iterators are identical."""
    while True:
        r_1, m_1, d_1 = next(timeseries_1, (DONE, None, None))
        r_2, m_2, d_2 = next(timeseries_2, (DONE, None, None))
        if r_1 == DONE and r_2 == DONE:
            return
        assert r_1 == r_2, f'{r_1} == {r_2}'
        assert m_1 == m_2, f'{m_1} == {m_2}'
        if d_1 is not None and d_2 is not None:
            assert_timeseries_equal(d_1, d_2)
        else:
            assert d_1 is None and d_2 is None


def assert_import_has_timeseries(etl_import: WaylayETLSeriesImport, timeseries: SeriesIterator = None):
    """Assert that a timeseries etl file has the given (or default) series in it."""
    with read_etl_import(etl_import) as timeseries_from_zip:
        assert_timeseries_data_equal(timeseries_from_zip, timeseries or default_timeseries_data())


SERIES_LENGTH = 3


def default_timeseries_data(metric_prefix: str = '') -> SeriesIterator:
    """Generate a dataset with two series.

    Test utility.
    """
    def timeseries():
        for i in range(SERIES_LENGTH):
            yield fromisoformat(f'1970-01-01T0{i}:00:00+00:00'), i

    yield 'test_resource', f'{metric_prefix}test_metric_1', timeseries()
    yield 'test_resource', f'{metric_prefix}test_metric_2', timeseries()
