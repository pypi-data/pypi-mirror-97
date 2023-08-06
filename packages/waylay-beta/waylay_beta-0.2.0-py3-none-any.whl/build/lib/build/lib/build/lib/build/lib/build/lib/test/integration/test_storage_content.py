"""Test storage content api."""
import httpx

from waylay import WaylayClient, RestResponseError


from waylay.service import StorageService

import pytest


def test_create_delete_content_objects(waylay_storage: StorageService):
    """Test put content."""
    result_1 = waylay_storage.content.put(
        'assets', 'test_folder/message.txt',
        content_type='text/plain',
        content='hello world!'
    )
    assert isinstance(result_1, str) and 'OK' in result_1

    result_2 = waylay_storage.object.stat('assets', 'test_folder/message.txt')
    assert result_2['name'] == 'test_folder/message.txt'
    assert result_2['size'] == 12

    result_3 = waylay_storage.content.get('assets', 'test_folder/message.txt')

    assert isinstance(result_3, httpx.Response) and result_3.text == 'hello world!'

    result_4 = waylay_storage.object.remove('assets', 'test_folder/message.txt')

    assert 'test_folder/message.txt' in result_4['_links']['removed']['href']

    with pytest.raises(RestResponseError) as exc_info:
        result_5 = waylay_storage.object.stat('assets', 'test_folder/message.txt')

    assert exc_info.value.response.status_code in (403, 404)
