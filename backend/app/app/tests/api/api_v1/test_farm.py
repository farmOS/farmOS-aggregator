import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.main import app
from app.core.config import Settings, settings
from app import utils
from app.core.jwt import create_farm_api_token
from app.tests.utils.utils import random_lower_string, get_scope_token_headers


@pytest.fixture
def farm_create_headers(client: TestClient):
    return get_scope_token_headers(client=client, scopes="farm:create")


@pytest.fixture
def farm_read_headers(client: TestClient):
    return get_scope_token_headers(client=client, scopes="farm:read")


@pytest.fixture
def farm_update_headers(client: TestClient):
    return get_scope_token_headers(client=client, scopes="farm:update")


@pytest.fixture
def farm_delete_headers(client: TestClient):
    return get_scope_token_headers(client=client, scopes="farm:delete")


def test_create_delete_farm(client: TestClient, db: Session, farm_create_headers, farm_delete_headers):
    farm_name = random_lower_string()
    url = 'test.farmos.net'

    # Provide a token on creation
    token = {
        'access_token': random_lower_string(),
        'expires_in': random_lower_string(),
        'refresh_token': random_lower_string(),
        'expires_at': 1581363344.0651991,
    }

    # Create a farm
    data = {
        "farm_name": farm_name,
        "url": url,
        "scope": 'user_access',
        "token": token,
    }
    r = client.post(
        f"{settings.API_V1_PREFIX}/farms/",
        headers=farm_create_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_farm = r.json()
    farm = crud.farm.get_by_id(db, farm_id=created_farm['id'])

    # Check that submitted values match those returned, and in db
    assert farm.farm_name == created_farm["farm_name"] == data['farm_name']
    assert farm.url == created_farm["url"] == data['url']

    # Check the created token.
    assert farm.token is not None
    assert 'token' in created_farm
    assert farm.token.access_token == created_farm['token']['access_token'] == token['access_token']
    assert farm.token.expires_in == created_farm['token']['expires_in'] == token['expires_in']
    assert farm.token.refresh_token == created_farm['token']['refresh_token'] == token['refresh_token']
    assert float(farm.token.expires_at) == created_farm['token']['expires_at'] == token['expires_at']

    # Delete the farm
    r = client.delete(
        f"{settings.API_V1_PREFIX}/farms/{farm.id}",
        headers=farm_delete_headers,
    )
    assert 200 <= r.status_code < 300


def test_create_farm_update_token(client: TestClient, db: Session, farm_create_headers, farm_update_headers, farm_delete_headers):
    farm_name = random_lower_string()
    url = 'test.farmos.net'

    # Create a farm
    data = {
        "farm_name": farm_name,
        "url": url,
        "scope": 'user_access',
    }
    r = client.post(
        f"{settings.API_V1_PREFIX}/farms/",
        headers=farm_create_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_farm = r.json()
    farm = crud.farm.get_by_id(db, farm_id=created_farm['id'])

    # Check that submitted values match those returned, and in db
    assert farm.farm_name == created_farm["farm_name"] == data['farm_name']
    assert farm.url == created_farm["url"] == data['url']
    assert farm.token is None

    # Provide a token on creation
    token = {
        'access_token': random_lower_string(),
        'expires_in': random_lower_string(),
        'refresh_token': random_lower_string(),
        'expires_at': 1581363344.0651991,
    }

    data = {
        "token": token,
    }
    r = client.put(
        f"{settings.API_V1_PREFIX}/farms/{farm.id}",
        headers=farm_update_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    updated_farm = r.json()
    # Refresh the object that was loaded previously
    db.refresh(farm)
    farm = crud.farm.get_by_id(db, farm_id=updated_farm['id'])

    assert farm.farm_name == updated_farm["farm_name"]
    assert farm.url == updated_farm["url"]

    # Check the token was created.
    assert 'token' in updated_farm
    assert farm.token is not None
    assert farm.token.access_token == updated_farm['token']['access_token'] == token['access_token']
    assert farm.token.expires_in == updated_farm['token']['expires_in'] == token['expires_in']
    assert farm.token.refresh_token == updated_farm['token']['refresh_token'] == token['refresh_token']
    assert float(farm.token.expires_at) == updated_farm['token']['expires_at'] == token['expires_at']

    # Delete the farm
    r = client.delete(
        f"{settings.API_V1_PREFIX}/farms/{farm.id}",
        headers=farm_delete_headers,
    )
    assert 200 <= r.status_code < 300


def test_create_farm_delete_token(client: TestClient, db: Session, farm_create_headers, farm_update_headers, farm_delete_headers):
    farm_name = random_lower_string()
    url = 'test.farmos.net'

    # Provide a token on creation
    token = {
        'access_token': random_lower_string(),
        'expires_in': random_lower_string(),
        'refresh_token': random_lower_string(),
        'expires_at': 1581363344.0651991,
    }

    # Create a farm
    data = {
        "farm_name": farm_name,
        "url": url,
        "scope": 'user_access',
        "token": token,
    }
    r = client.post(
        f"{settings.API_V1_PREFIX}/farms/",
        headers=farm_create_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_farm = r.json()
    farm = crud.farm.get_by_id(db, farm_id=created_farm['id'])

    # Check that submitted values match those returned, and in db
    assert farm.farm_name == created_farm["farm_name"] == data['farm_name']
    assert farm.url == created_farm["url"] == data['url']

    # Check the created token.
    assert farm.token is not None
    assert 'token' in created_farm
    assert farm.token.access_token == created_farm['token']['access_token'] == token['access_token']
    assert farm.token.expires_in == created_farm['token']['expires_in'] == token['expires_in']
    assert farm.token.refresh_token == created_farm['token']['refresh_token'] == token['refresh_token']
    assert float(farm.token.expires_at) == created_farm['token']['expires_at'] == token['expires_at']

    # Provide a token on creation
    new_token = {}

    data = {
        "token": new_token,
    }
    r = client.put(
        f"{settings.API_V1_PREFIX}/farms/{farm.id}",
        headers=farm_update_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    updated_farm = r.json()
    # Refresh the object that was loaded previously
    db.refresh(farm)
    farm = crud.farm.get_by_id(db, farm_id=updated_farm['id'])

    assert farm.farm_name == updated_farm["farm_name"]
    assert farm.url == updated_farm["url"]

    # Check the token WAS NOT deleted
    assert 'token' in updated_farm
    assert farm.token is not None
    assert farm.token.access_token == updated_farm['token']['access_token'] == token['access_token']
    assert farm.token.expires_in == updated_farm['token']['expires_in'] == token['expires_in']
    assert farm.token.refresh_token == updated_farm['token']['refresh_token'] == token['refresh_token']
    assert float(farm.token.expires_at) == updated_farm['token']['expires_at'] == token['expires_at']

    # Delete the farm
    r = client.delete(
        f"{settings.API_V1_PREFIX}/farms/{farm.id}",
        headers=farm_delete_headers,
    )
    assert 200 <= r.status_code < 300


def test_get_all_farms(client: TestClient, db: Session, test_farm, farm_read_headers):
    farm_id = test_farm.id
    r = client.get(
        f"{settings.API_V1_PREFIX}/farms/",
        headers=farm_read_headers,
    )
    assert 200 <= r.status_code < 300
    response = r.json()
    first_id = response[0]['id']
    farm = crud.farm.get_by_id(db, farm_id=first_id)
    assert farm.farm_name == response[0]["farm_name"]


def test_get_farm_by_id(client: TestClient, db: Session, test_farm, farm_read_headers):
    farm_id = test_farm.id
    r = client.get(
        f"{settings.API_V1_PREFIX}/farms/{farm_id}",
        headers=farm_read_headers,
    )
    assert 200 <= r.status_code < 300
    response = r.json()
    farm = crud.farm.get_by_id(db, farm_id=response['id'])
    assert farm.farm_name == response["farm_name"]


def test_farm_create_oauth_scope():
    def settings_open_registration():
        return Settings(AGGREGATOR_OPEN_FARM_REGISTRATION=True, AGGREGATOR_INVITE_FARM_REGISTRATION=True)

    def settings_invite_registration():
        return Settings(AGGREGATOR_OPEN_FARM_REGISTRATION=False, AGGREGATOR_INVITE_FARM_REGISTRATION=True)

    def settings_closed_registration():
        return Settings(AGGREGATOR_OPEN_FARM_REGISTRATION=False, AGGREGATOR_INVITE_FARM_REGISTRATION=False)

    client = TestClient(app)

    # Disable Open Farm Registration, assert the endpoint is not publicly accessible.
    app.dependency_overrides[utils.get_settings] = settings_closed_registration
    r = client.post(f"{settings.API_V1_PREFIX}/farms/")
    assert r.status_code == 401

    # Disable Invite Farm Registration, assert the endpoint is not accessible with access token.
    token = create_farm_api_token(farm_id=[], scopes=["farm:create", "farm:info"])
    app.dependency_overrides[utils.get_settings] = settings_closed_registration
    r = client.post(
        f"{settings.API_V1_PREFIX}/farms/",
        headers={"api-token": token.decode("utf-8")}
    )
    assert r.status_code == 401

    # Enable Invite Farm Registration, assert the endpoint is not publicly accessible.
    app.dependency_overrides[utils.get_settings] = settings_invite_registration
    r = client.post(f"{settings.API_V1_PREFIX}/farms/")
    assert r.status_code == 401

    # Enable Invite Farm Registration, assert the endpoint is accessible with access token.
    token = create_farm_api_token(farm_id=[], scopes=["farm:create", "farm:info"])
    app.dependency_overrides[utils.get_settings] = settings_invite_registration
    r = client.post(
        f"{settings.API_V1_PREFIX}/farms/",
        headers={"api-token": token.decode("utf-8")}
    )
    assert r.status_code == 422

    # Enable Open Farm Registration, assert the endpoint is publicly accessible.
    app.dependency_overrides[utils.get_settings] = settings_open_registration
    r = client.post(f"{settings.API_V1_PREFIX}/farms/")
    assert r.status_code == 422


def test_farm_read_oauth_scope(client: TestClient):
    r = client.get(f"{settings.API_V1_PREFIX}/farms/")
    assert r.status_code == 401


def test_farm_read_by_id_oauth_scope(client: TestClient):
    r = client.get(f"{settings.API_V1_PREFIX}/farms/1")
    assert r.status_code == 401


def test_farm_update_oauth_scope(client: TestClient):
    r = client.put(f"{settings.API_V1_PREFIX}/farms/1")
    assert r.status_code == 401


def test_farm_delete_oauth_scope(client: TestClient):
    r = client.get(f"{settings.API_V1_PREFIX}/farms/1")
    assert r.status_code == 401
