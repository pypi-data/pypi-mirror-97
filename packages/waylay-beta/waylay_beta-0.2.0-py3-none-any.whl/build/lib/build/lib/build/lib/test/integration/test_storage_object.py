"""Object Storage api tests."""

from waylay import WaylayClient, RestResponseError
from waylay.service import StorageService

import pytest


def test_list_objects(waylay_storage: StorageService):
    """Test storage list api."""
    result = waylay_storage.object.list('assets', '')
    assert isinstance(result, list)


def test_create_remove_folder(waylay_storage: StorageService):
    """Test storage remove folder api."""
    result = waylay_storage.folder.create('assets', 'integration_test/test_folder')

    assert result is not None
    result = waylay_storage.folder.stat('assets', 'integration_test/test_folder')
    assert result['bucket']['alias'] == 'assets'
    assert result['name'] == 'integration_test/test_folder/'

    result = waylay_storage.folder.remove('assets', 'integration_test/test_folder')
    assert result is not None


def test_sign_get(waylay_storage: StorageService):
    """Test storage sign get api."""
    sign_get = waylay_storage.object.sign_get('assets', 'integration_test/test_folder')
    assert sign_get is not None
    assert 'integration_test/test_folder' in sign_get


def test_sign_put(waylay_storage: StorageService):
    """Test storage sign put api."""
    sign_put = waylay_storage.object.sign_put('assets', 'integration_test/test_folder')
    assert sign_put is not None
    assert 'integration_test/test_folder' in sign_put


def test_sign_post(waylay_storage: StorageService):
    """Test storage sign post api."""
    sign_post = waylay_storage.object.sign_post('assets', 'integration_test/test_folder')
    assert sign_post is not None
    assert sign_post['href'] is not None
    assert sign_post['method'] == 'POST'
    assert 'integration_test/test_folder' in sign_post['form_data']['key']


def test_iter_list_all(waylay_storage: StorageService):
    """Test storage paging list api."""
    non_paging_list = waylay_storage.object.list('assets', '', params=dict(recursive=True, max_keys=2))
    assert len(non_paging_list) == 2

    object_iterator = waylay_storage.object.iter_list_all(
        'assets', '', params=dict(recursive=True, max_keys=2)
    )
    assert next(object_iterator) is not None
    assert next(object_iterator) is not None
    # a third object should be in the interator
    assert next(object_iterator) is not None
