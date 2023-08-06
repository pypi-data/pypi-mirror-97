"""Integration tests for waylay.service.analytics module."""
import csv
from datetime import datetime

import pytest

from waylay import WaylayClient
from waylay.exceptions import RestError


def test_analytics_query_json(waylay_test_client: WaylayClient):
    """Execute query with json response."""
    data_resp = waylay_test_client.analytics.query.data('151CF-temperature', raw=True).body
    assert data_resp is not None
    assert 'data' in data_resp
    assert len(data_resp['data']) == 1
    assert 'columns' in data_resp['data'][0]


def test_analytics_query_df(waylay_test_client: WaylayClient):
    """Execute query with dataframe response."""
    data_df = waylay_test_client.analytics.query.data('151CF-temperature')
    assert data_df is not None
    assert data_df.columns.names == ['resource', 'metric', 'aggregation']
    assert data_df.size > 0


def test_analytics_query_df_no_data(waylay_test_client: WaylayClient):
    """Execute query with empty result set."""
    data_df = waylay_test_client.analytics.query.data('151CF-temperature', params={
        'from': '2010-10-10',
        'window': 'P1D',
    })
    assert data_df is not None


def test_analytics_execute_query_df_no_aggr_no_data(waylay_test_client: WaylayClient):
    """Excecute query for non-existing resource."""
    data_df = waylay_test_client.analytics.query.execute(body={
        "resource": "doesnotexist",
        "from": "2010-10-10",
        "until": "2010-10-11",
        "data": [
            {"metric": "colourfullness"},
            {"metric": "playfullness"}
        ]
    })
    assert data_df is not None
    assert data_df.size == 0


def test_analytics_query_csv(waylay_test_client: WaylayClient):
    """Execute a query with json response."""
    query = waylay_test_client.analytics.query.get('151CF-temperature', raw=True).body['query']
    data_resp = waylay_test_client.analytics.query.data(
        '151CF-temperature', raw=True, params={'render.mode': 'RENDER_MODE_CSV'}).body
    assert isinstance(data_resp, str)
    reader = csv.reader(data_resp.splitlines(), delimiter=',')
    header = next(reader)
    assert isinstance(header, list)
    potential_column_names = ['timestamp'] + [
        series.get(
            'name',
            series.get(
                'resource', query.get('resource')
            ) + '/' + series.get(
                'metric',  query.get('metric')
            )
        ) for series in query['data']
    ]
    for col in header:
        assert col in potential_column_names


def test_crud_query(waylay_test_client: WaylayClient):
    """Create, read , update and delete a query."""
    query_name = f'integration_test_{datetime.now().timestamp()}'
    query = {
        "resource": "doesnotexist",
        "from": "2010-10-10",
        "until": "2010-10-11",
        "data": [
                {"metric": "colourfullness"},
                {"metric": "playfullness"}
        ]
    }
    result = waylay_test_client.analytics.query.create(body={
        "name": query_name,
        "query": query
    })
    assert result == query

    assert waylay_test_client.analytics.query.get(query_name) == query

    query['resource'] = 'surelydoesntexist'
    assert waylay_test_client.analytics.query.replace(query_name, body={"query": query}) == query

    query['resource'] = 'stillnotexists'
    with pytest.raises(RestError) as exc_info:
        waylay_test_client.analytics.query.replace(
            query_name, body={"name": query_name, "query": query}
        )
    assert 'Name should not be specified when using PUT' in format(exc_info.value)

    result = waylay_test_client.analytics.query.remove(query_name)
    assert result is not None
