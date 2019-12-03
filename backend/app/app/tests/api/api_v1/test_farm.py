import requests
import pytest

from app import crud
from app.core import config
from app.db.session import db_session
from app.models.farm import FarmCreate
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
    username = random_lower_string()
    password = random_lower_string()

    # Create a farm
    data = {
        "farm_name": farm_name,
        "url": url,
        "username": username,
        "password": password
    }
    r = requests.post(
        f"{server_api}{config.API_V1_STR}/farms/",
        headers=farm_create_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_farm = r.json()
    farm = crud.farm.get_by_id(db_session, farm_id=created_farm['id'])
    assert farm.farm_name == created_farm["farm_name"]

    # Delete the farm
    r = requests.delete(
        f"{server_api}{config.API_V1_STR}/farms/{farm.id}",
        headers=farm_delete_headers,
    )
    assert 200 <= r.status_code < 300


def test_get_all_farms(test_farm, farm_read_headers):
    server_api = get_server_api()

    farm_id = test_farm.id
    r = requests.get(
        f"{server_api}{config.API_V1_STR}/farms/",
        headers=farm_read_headers,
    )
    assert 200 <= r.status_code < 300
    response = r.json()
    first_id = response[0]['id']
    farm = crud.farm.get_by_id(db_session, farm_id=first_id)
    assert farm.farm_name == response[0]["farm_name"]
    assert not hasattr(response[0], 'password')


def test_get_farm_by_id(test_farm, farm_read_headers):
    server_api = get_server_api()

    farm_id = test_farm.id
    r = requests.get(
        f"{server_api}{config.API_V1_STR}/farms/{farm_id}",
        headers=farm_read_headers,
    )
    assert 200 <= r.status_code < 300
    response = r.json()
    farm = crud.farm.get_by_id(db_session, farm_id=response['id'])
    assert farm.farm_name == response["farm_name"]
    assert not hasattr(response, 'password')


def test_farm_create_oauth_scope():
    server_api = get_server_api()

    r = requests.post(f"{server_api}{config.API_V1_STR}/farms/")
    assert r.status_code == 401


def test_farm_read_oauth_scope():
    server_api = get_server_api()

    r = requests.get(f"{server_api}{config.API_V1_STR}/farms/")
    assert r.status_code == 401


def test_farm_read_by_id_oauth_scope():
    server_api = get_server_api()

    r = requests.get(f"{server_api}{config.API_V1_STR}/farms/1")
    assert r.status_code == 401


def test_farm_update_oauth_scope():
    server_api = get_server_api()

    r = requests.put(f"{server_api}{config.API_V1_STR}/farms/1")
    assert r.status_code == 401


def test_farm_delete_oauth_scope():
    server_api = get_server_api()

    r = requests.get(f"{server_api}{config.API_V1_STR}/farms/1")
    assert r.status_code == 401
