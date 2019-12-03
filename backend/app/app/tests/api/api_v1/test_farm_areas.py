import requests
import pytest

from app.core import config
from app.tests.utils.utils import get_server_api, get_scope_token_headers


@pytest.fixture
def farm_areas_headers():
    return get_scope_token_headers("farm:read farm.areas")


def test_create_area(test_farm, test_area, farm_areas_headers):
    server_api = get_server_api()

    data = test_area

    response = requests.post(
        f"{server_api}{config.API_V1_STR}/farms/areas/?farm_id={test_farm.id}",
        headers=farm_areas_headers,
        json=data,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()

    # Check farm ID included in response
    assert str(test_farm.id) in content

    # Check area was created
    test_farm_areas = content[str(test_farm.id)]
    assert len(test_farm_areas) == 1
    assert 'id' in test_farm_areas[0]
    created_area_id = test_farm_areas[0]['id']
    test_area['id'] = created_area_id

    # Check that the created area has correct attributes
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/farms/areas/?farm_id={test_farm.id}&tid={test_area['id']}",
        headers=farm_areas_headers,
        json=data,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()
    assert str(test_farm.id) in content
    assert len(content[str(test_farm.id)]) == 1
    created_area = content[str(test_farm.id)][0]
    # Check attributes
    assert created_area['area_type'] == data['area_type']
    # Check that an optional attribute was populated
    assert data['description'] in created_area['description']


def test_get_areas(test_farm, farm_areas_headers):
    server_api = get_server_api()

    r = requests.get(
        f"{server_api}{config.API_V1_STR}/farms/areas/?farm_id={test_farm.id}",
        headers=farm_areas_headers,
    )
    # Check response
    assert 200 <= r.status_code < 300
    areas = r.json()

    # Check farm ID included in response
    assert str(test_farm.id) in areas

    # Check areas are returned for the farm
    test_farm_areas = areas[str(test_farm.id)]
    assert len(test_farm_areas) > 1
    for area in test_farm_areas:
        assert "area_type" in area

    assert str(test_farm.id) in areas

    test_farm_areas = areas[str(test_farm.id)]
    assert len(test_farm_areas) > 1
    for area in test_farm_areas:
        assert "area_type" in area


def test_update_area(test_farm, test_area, farm_areas_headers):
    server_api = get_server_api()

    # Change area attributes
    test_area['name'] = "Updated name from farmOS-aggregator"
    test_area['description'] = "Update description"
    data = test_area

    response = requests.put(
        f"{server_api}{config.API_V1_STR}/farms/areas/?farm_id={test_farm.id}",
        headers=farm_areas_headers,
        json=data,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()

    # Check farm ID included in response
    assert str(test_farm.id) in content
    assert len(content[str(test_farm.id)]) == 1
    response_area = content[str(test_farm.id)][0]
    assert 'id' in response_area
    assert test_area['id'] == str(response_area['id'])

    # Check that the updated area has correct attributes
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/farms/areas/?farm_id={test_farm.id}&tid={test_area['id']}",
        headers=farm_areas_headers,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()
    assert str(test_farm.id) in content
    assert len(content[str(test_farm.id)]) == 1
    updated_area = content[str(test_farm.id)][0]
    # Check attributes
    assert updated_area['name'] == data['name']
    # Check that an optional attribute was updated
    assert data['description'] in updated_area['description']


def test_delete_area(test_farm, test_area, farm_areas_headers):
    server_api = get_server_api()

    response = requests.delete(
        f"{server_api}{config.API_V1_STR}/farms/areas/?farm_id={test_farm.id}&id={test_area['id']}",
        headers=farm_areas_headers,
    )

    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()


def test_farm_areas_oauth_scope():
    server_api = get_server_api()

    r = requests.get(f"{server_api}{config.API_V1_STR}/farms/areas")
    assert r.status_code == 401
