import requests
import pytest

from app import crud
from app.core.config import settings
from app.db.session import db_session
from app.schemas.farm import FarmCreate
from app.tests.utils.utils import get_server_api, random_lower_string, get_scope_token_headers


@pytest.fixture
def farm_create_headers():
    return get_scope_token_headers("farm:create")


@pytest.fixture
def farm_read_headers():
    return get_scope_token_headers("farm:read")


@pytest.fixture
def farm_update_headers():
    return get_scope_token_headers("farm:update")


@pytest.fixture
def farm_delete_headers():
    return get_scope_token_headers("farm:delete")


def test_create_delete_farm(farm_create_headers, farm_delete_headers):
    server_api = get_server_api()

    farm_name = random_lower_string()
    url = 'test.farmos.net'

    # Provide a token on creation
    token = {
        'access_token': random_lower_string(),
        'expires_in': random_lower_string(),
        'refresh_token': random_lower_string(),
        'expires_at': random_lower_string(),
    }

    # Create a farm
    data = {
        "farm_name": farm_name,
        "url": url,
        "scope": 'user_access',
        "token": token,
    }
    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/farms/",
        headers=farm_create_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_farm = r.json()
    farm = crud.farm.get_by_id(db_session, farm_id=created_farm['id'])

    # Check that submitted values match those returned, and in db
    assert farm.farm_name == created_farm["farm_name"] == data['farm_name']
    assert farm.url == created_farm["url"] == data['url']

    # Check the created token.
    assert farm.token is not None
    assert 'token' in created_farm
    assert farm.token.access_token == created_farm['token']['access_token'] == token['access_token']
    assert farm.token.expires_in == created_farm['token']['expires_in'] == token['expires_in']
    assert farm.token.refresh_token == created_farm['token']['refresh_token'] == token['refresh_token']
    assert farm.token.expires_at == created_farm['token']['expires_at'] == token['expires_at']

    # Delete the farm
    r = requests.delete(
        f"{server_api}{settings.API_V1_STR}/farms/{farm.id}",
        headers=farm_delete_headers,
    )
    assert 200 <= r.status_code < 300


def test_create_farm_update_token(farm_create_headers, farm_update_headers, farm_delete_headers):
    server_api = get_server_api()

    farm_name = random_lower_string()
    url = 'test.farmos.net'

    # Create a farm
    data = {
        "farm_name": farm_name,
        "url": url,
        "scope": 'user_access',
    }
    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/farms/",
        headers=farm_create_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_farm = r.json()
    farm = crud.farm.get_by_id(db_session, farm_id=created_farm['id'])

    # Check that submitted values match those returned, and in db
    assert farm.farm_name == created_farm["farm_name"] == data['farm_name']
    assert farm.url == created_farm["url"] == data['url']
    assert farm.token is None

    # Provide a token on creation
    token = {
        'access_token': random_lower_string(),
        'expires_in': random_lower_string(),
        'refresh_token': random_lower_string(),
        'expires_at': random_lower_string(),
    }

    data = {
        "token": token,
    }
    r = requests.put(
        f"{server_api}{settings.API_V1_STR}/farms/{farm.id}",
        headers=farm_update_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    updated_farm = r.json()
    # Refresh the object that was loaded previously
    db_session.refresh(farm)
    farm = crud.farm.get_by_id(db_session, farm_id=updated_farm['id'])

    assert farm.farm_name == updated_farm["farm_name"]
    assert farm.url == updated_farm["url"]

    # Check the token was created.
    assert 'token' in updated_farm
    assert farm.token is not None
    assert farm.token.access_token == updated_farm['token']['access_token'] == token['access_token']
    assert farm.token.expires_in == updated_farm['token']['expires_in'] == token['expires_in']
    assert farm.token.refresh_token == updated_farm['token']['refresh_token'] == token['refresh_token']
    assert farm.token.expires_at == updated_farm['token']['expires_at'] == token['expires_at']

    # Delete the farm
    r = requests.delete(
        f"{server_api}{settings.API_V1_STR}/farms/{farm.id}",
        headers=farm_delete_headers,
    )
    assert 200 <= r.status_code < 300


def test_create_farm_delete_token(farm_create_headers, farm_update_headers, farm_delete_headers):
    server_api = get_server_api()

    farm_name = random_lower_string()
    url = 'test.farmos.net'

    # Provide a token on creation
    token = {
        'access_token': random_lower_string(),
        'expires_in': random_lower_string(),
        'refresh_token': random_lower_string(),
        'expires_at': random_lower_string(),
    }

    # Create a farm
    data = {
        "farm_name": farm_name,
        "url": url,
        "scope": 'user_access',
        "token": token,
    }
    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/farms/",
        headers=farm_create_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_farm = r.json()
    farm = crud.farm.get_by_id(db_session, farm_id=created_farm['id'])

    # Check that submitted values match those returned, and in db
    assert farm.farm_name == created_farm["farm_name"] == data['farm_name']
    assert farm.url == created_farm["url"] == data['url']

    # Check the created token.
    assert farm.token is not None
    assert 'token' in created_farm
    assert farm.token.access_token == created_farm['token']['access_token'] == token['access_token']
    assert farm.token.expires_in == created_farm['token']['expires_in'] == token['expires_in']
    assert farm.token.refresh_token == created_farm['token']['refresh_token'] == token['refresh_token']
    assert farm.token.expires_at == created_farm['token']['expires_at'] == token['expires_at']

    # Provide a token on creation
    new_token = {}

    data = {
        "token": new_token,
    }
    r = requests.put(
        f"{server_api}{settings.API_V1_STR}/farms/{farm.id}",
        headers=farm_update_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    updated_farm = r.json()
    # Refresh the object that was loaded previously
    db_session.refresh(farm)
    farm = crud.farm.get_by_id(db_session, farm_id=updated_farm['id'])

    assert farm.farm_name == updated_farm["farm_name"]
    assert farm.url == updated_farm["url"]

    # Check the token WAS NOT deleted
    assert 'token' in updated_farm
    assert farm.token is not None
    assert farm.token.access_token == updated_farm['token']['access_token'] == token['access_token']
    assert farm.token.expires_in == updated_farm['token']['expires_in'] == token['expires_in']
    assert farm.token.refresh_token == updated_farm['token']['refresh_token'] == token['refresh_token']
    assert farm.token.expires_at == updated_farm['token']['expires_at'] == token['expires_at']

    # Delete the farm
    r = requests.delete(
        f"{server_api}{settings.API_V1_STR}/farms/{farm.id}",
        headers=farm_delete_headers,
    )
    assert 200 <= r.status_code < 300


def test_get_all_farms(test_farm, farm_read_headers):
    server_api = get_server_api()

    farm_id = test_farm.id
    r = requests.get(
        f"{server_api}{settings.API_V1_STR}/farms/",
        headers=farm_read_headers,
    )
    assert 200 <= r.status_code < 300
    response = r.json()
    first_id = response[0]['id']
    farm = crud.farm.get_by_id(db_session, farm_id=first_id)
    assert farm.farm_name == response[0]["farm_name"]


def test_get_farm_by_id(test_farm, farm_read_headers):
    server_api = get_server_api()

    farm_id = test_farm.id
    r = requests.get(
        f"{server_api}{settings.API_V1_STR}/farms/{farm_id}",
        headers=farm_read_headers,
    )
    assert 200 <= r.status_code < 300
    response = r.json()
    farm = crud.farm.get_by_id(db_session, farm_id=response['id'])
    assert farm.farm_name == response["farm_name"]

"""
Skip this test for now. Need more settings to test settingsurable public/private endpoints.
def test_farm_create_oauth_scope():
    server_api = get_server_api()

    r = requests.post(f"{server_api}{settings.API_V1_STR}/farms/")
    assert r.status_code == 401
"""


def test_farm_read_oauth_scope():
    server_api = get_server_api()

    r = requests.get(f"{server_api}{settings.API_V1_STR}/farms/")
    assert r.status_code == 401


def test_farm_read_by_id_oauth_scope():
    server_api = get_server_api()

    r = requests.get(f"{server_api}{settings.API_V1_STR}/farms/1")
    assert r.status_code == 401


def test_farm_update_oauth_scope():
    server_api = get_server_api()

    r = requests.put(f"{server_api}{settings.API_V1_STR}/farms/1")
    assert r.status_code == 401


def test_farm_delete_oauth_scope():
    server_api = get_server_api()

    r = requests.get(f"{server_api}{settings.API_V1_STR}/farms/1")
    assert r.status_code == 401
