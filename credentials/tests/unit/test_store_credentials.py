import json

import pytest
from unittest.mock import Mock

from credentials import store_credentials
from unittest import result
import sys

sys.path.append("../../credentials")
@pytest.fixture()
def store_credentials_event():
    return { 
            "id":"sample-id",
            "access_token":"sample-access-token",
            "refresh_token":"sample-refresh-token",
            "credential_type":"athlete",
            "expires_at":"2024-01-01"
        }

@pytest.fixture()
def store_app_credentials_event():
    return { 
            "id":"sample-id",
            "application_id":"sample-application-id",
            "application_secret":"sample-application-secret",
            "credential_type":"application"
        }


@pytest.fixture()
def store_app_credentials_event_invalid_type():
    return { 
            "id":"sample-id",
            "application_id":"sample-application-id",
            "application_secret":"sample-application-secret",
            "credential_type":"invalid-credential-type"
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
        pytest.fail(f"Unexpected exception: {str(e)}",e)

def test_store_app_credentials(store_app_credentials_event, mocker):
    try:
        result = store_credentials.write_credentials(store_app_credentials_event, mocker)
        assert result['id'] == store_app_credentials_event['id']
        assert result['status'] == 'success'
    except Exception as e:
        pytest.fail(f"Unexpected exception: {str(e)}",e)

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

def test_store_credentials_invalid_event_type(store_app_credentials_event_invalid_type,mocker):
    with pytest.raises(Exception):
        store_credentials.write_credentials(store_app_credentials_event_invalid_type, mocker)