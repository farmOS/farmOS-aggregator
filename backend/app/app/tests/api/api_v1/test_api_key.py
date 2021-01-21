from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.utils import random_lower_string, get_api_key_headers
from app.schemas.api_key import ApiKeyCreate, ApiKeyUpdate


def test_create_update_delete_api_key(client: TestClient, superuser_token_headers):
    api_key = ApiKeyCreate(
        name="Test Key",
        all_farms=True,
        farm_id=[0,1,2],
        notes="Some notes",
        enabled=True
    )

    r = client.post(
        f"{settings.API_V1_PREFIX}/api-keys/",
        headers=superuser_token_headers,
        data=api_key.json()
    )
    assert 200 <= r.status_code < 300

    key = r.json()
    assert key
    assert "id" in key
    assert "key" in key
    assert key["enabled"] == api_key.enabled
    assert key["farm_id"] == api_key.farm_id
    assert key["all_farms"] == api_key.all_farms
    assert key["name"] == api_key.name
    assert key["notes"] == api_key.notes

    # Update the key
    key_update = ApiKeyUpdate(
        name="My New Name",
        enabled=False,
        notes="Updated notes",
        all_farms=False,
        farm_id=[]
    )
    r = client.put(
        f"{settings.API_V1_PREFIX}/api-keys/{key['id']}",
        headers=superuser_token_headers,
        data=key_update.json()
    )
    assert 200 <= r.status_code < 300
    updated_key = r.json()

    assert updated_key
    assert "key" in updated_key
    assert updated_key["enabled"] == key_update.enabled
    assert updated_key["name"] == key_update.name
    assert updated_key["notes"] == key_update.notes

    # Check that these values did not change.
    assert updated_key["farm_id"] == api_key.farm_id
    assert updated_key["all_farms"] == api_key.all_farms

    # Delete API Key.
    r = client.delete(
        f"{settings.API_V1_PREFIX}/api-keys/{key['id']}",
        headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300


def test_get_api_keys(client: TestClient, superuser_token_headers):
    r = client.get(
        f"{settings.API_V1_PREFIX}/users/me", headers=superuser_token_headers
    )
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_read_farms_all_farms_api_key(client: TestClient, db: Session, test_farm):
    test_api_key = ApiKeyCreate(
        name="Test Key",
        enabled=True,
        all_farms=True,
        scopes=["farm:read"]
    )

    farm_id = test_farm.id
    r = client.get(
        f"{settings.API_V1_PREFIX}/farms/{farm_id}",
        headers=get_api_key_headers(client=client, api_key_params=test_api_key),
    )
    assert 200 <= r.status_code < 300
    response = r.json()
    farm = crud.farm.get_by_id(db, farm_id=response['id'])
    assert farm.farm_name == response["farm_name"]


def test_read_farms_one_farm_id_api_key(client: TestClient, db: Session, test_farm):
    test_api_key = ApiKeyCreate(
        name="Test Key",
        enabled=True,
        farm_id=[test_farm.id],
        scopes=["farm:read"]
    )

    farm_id = test_farm.id
    r = client.get(
        f"{settings.API_V1_PREFIX}/farms/{farm_id}",
        headers=get_api_key_headers(client=client, api_key_params=test_api_key),
    )
    assert 200 <= r.status_code < 300
    response = r.json()
    farm = crud.farm.get_by_id(db, farm_id=response['id'])
    assert farm.farm_name == response["farm_name"]


def test_read_farms_wrong_farm_id_api_key(client: TestClient, test_farm):
    test_api_key = ApiKeyCreate(
        name="Test Key",
        enabled=True,
        farm_id=[99],
        scopes=["farm:read"]
    )

    farm_id = test_farm.id
    r = client.get(
        f"{settings.API_V1_PREFIX}/farms/{farm_id}",
        headers=get_api_key_headers(client=client, api_key_params=test_api_key),
    )
    assert r.status_code == 401


def test_read_farms_no_farms_api_key(client: TestClient, test_farm):
    test_api_key = ApiKeyCreate(
        name="Test Key",
        enabled=True,
        all_farms=False,
        scopes=["farm:read"]
    )

    farm_id = test_farm.id
    r = client.get(
        f"{settings.API_V1_PREFIX}/farms/{farm_id}",
        headers=get_api_key_headers(client=client, api_key_params=test_api_key),
    )
    assert r.status_code == 401


def test_read_farms_disabled_api_key(client: TestClient, test_farm):
    test_api_key = ApiKeyCreate(
        name="Test Key",
        enabled=False,
        all_farms=True,
        scopes=["farm:read"]
    )

    farm_id = test_farm.id
    r = client.get(
        f"{settings.API_V1_PREFIX}/farms/{farm_id}",
        headers=get_api_key_headers(client=client, api_key_params=test_api_key),
    )
    assert r.status_code == 401


def test_read_farms_no_scope_api_key(client: TestClient, test_farm):
    test_api_key = ApiKeyCreate(
        name="Test Key",
        enabled=True,
        all_farms=True,
        scopes=[]
    )

    farm_id = test_farm.id
    r = client.get(
        f"{settings.API_V1_PREFIX}/farms/{farm_id}",
        headers=get_api_key_headers(client=client, api_key_params=test_api_key),
    )
    assert r.status_code == 401


def test_read_farms_random_api_key(client: TestClient, test_farm):
    farm_id = test_farm.id
    r = client.get(
        f"{settings.API_V1_PREFIX}/farms/{farm_id}",
        headers={"api-key": f"{random_lower_string()}"},
    )
    assert r.status_code == 401
