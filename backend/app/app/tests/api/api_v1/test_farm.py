import requests

from app import crud
from app.core import config
from app.db.session import db_session
from app.models.farm import FarmInCreate
from app.tests.utils.utils import get_server_api, random_lower_string

def test_create_delete_farm():
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
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_farm = r.json()
    farm = crud.farm.get_by_id(db_session, farm_id=created_farm['id'])
    assert farm.farm_name == created_farm["farm_name"]

    # Delete the farm
    r = requests.delete(
        f"{server_api}{config.API_V1_STR}/farms/{farm.id}",

    )
    assert 200 <= r.status_code < 300

def test_get_existing_farm(test_farm):
    server_api = get_server_api()

    farm_id = test_farm.id
    r = requests.get(
        f"{server_api}{config.API_V1_STR}/farms/{farm_id}",
    )
    assert 200 <= r.status_code < 300
    api_farm = r.json()
    farm = crud.farm.get_by_id(db_session, farm_id=api_farm['id'])
    assert farm.farm_name == api_farm["farm_name"]
