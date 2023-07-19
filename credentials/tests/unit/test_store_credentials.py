import json

import pytest
from unittest.mock import Mock

from credentials import store_credentials
from unittest import result


@pytest.fixture()
def store_credentials_event():
    return { 
            "id":"sample-id",
            "access_token":"sample-access-token",
            "refresh_token":"sample-refresh-token",
            "credential_type":"sample-credentials-type",
            "expires_at":"2024-01-01"
        }
@pytest.fixture()
def mocker():
    return Mock()

def test_store_credentials(store_credentials_event, mocker):
    try:
        result = store_credentials.write_credentials(store_credentials_event, mocker)
        assert result['id'] == store_credentials_event['id']
        assert result['status'] == 'success'
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")


def test_store_credentials_invalid_event(mocker):
    with pytest.raises(Exception):
        store_credentials.write_credentials({}, mocker)

def test_store_credentials_invalid_event_type(mocker):
    with pytest.raises(Exception):
        store_credentials.write_credentials(1, mocker)
def test_store_credentials_ddb_exception(store_credentials_event, mocker):
    mocker.put_item.side_effect = Exception()
    with pytest.raises(Exception):
        store_credentials.write_credentials(store_credentials_event, mocker)