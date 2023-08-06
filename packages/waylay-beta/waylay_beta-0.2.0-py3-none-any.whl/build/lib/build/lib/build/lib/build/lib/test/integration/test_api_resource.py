"""Check setup of a waylay client."""

from waylay import WaylayClient, RestResponseError

from waylay.service import ApiService

TEST_RESOURCE_ID = 'waylay-py-integration-test'


def test_api_resource(waylay_api: ApiService):
    """Test all exposed methods of the /api/resources engine api."""
    assert waylay_api.root_url is not None
    resource_api = waylay_api.resource

    try:
        result = resource_api.remove(TEST_RESOURCE_ID)
    except RestResponseError as e:
        # not existing
        assert e.response.status_code == 404

    result = resource_api.create(body={'id': TEST_RESOURCE_ID})

    result = resource_api.get(TEST_RESOURCE_ID)
    assert result['id'] == TEST_RESOURCE_ID

    result = resource_api.replace(TEST_RESOURCE_ID, body={
        'id': TEST_RESOURCE_ID, 'name': TEST_RESOURCE_ID
    })
    assert result['id'] == TEST_RESOURCE_ID

    result = resource_api.update(
        TEST_RESOURCE_ID, body={'metrics': [dict(name='temp')]
                                })
    assert result['metrics'][0]['name'] == 'temp'

    result = resource_api.search(params=dict(filter=TEST_RESOURCE_ID))
    assert len(result) == 1
    assert result[0]['id'] == TEST_RESOURCE_ID

    result = resource_api.remove(TEST_RESOURCE_ID)
    assert result is None
