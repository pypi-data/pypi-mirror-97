"""Test storage bucket api."""

from waylay import WaylayClient, RestResponseError

from waylay.service import StorageService


def test_list_buckets(waylay_storage: StorageService):
    """Test listing of storage buckets."""
    result = waylay_storage.bucket.list()

    assert result is not None

    bucket_aliases = [bucket['alias'] for bucket in result]
    assert 'public' in bucket_aliases
    assert 'etl-import' in bucket_aliases
    assert 'etl-export' in bucket_aliases


def test_get_bucket(waylay_storage: StorageService):
    """Test retrieval of storage bucket."""
    result = waylay_storage.bucket.get('etl-import')

    assert result is not None
    assert result['alias'] == 'etl-import'
