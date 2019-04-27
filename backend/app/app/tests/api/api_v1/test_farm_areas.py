import requests

from app import crud
from app.core import config
from app.db.session import db_session
from app.tests.utils.utils import get_server_api, random_lower_string

def test_create_area(test_farm, test_area):
    server_api = get_server_api()

    data = test_area

    response = requests.post(
        f"{server_api}{config.API_V1_STR}/farms/areas/?farms={test_farm.id}",
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

    # Check that the creats area has correct attributes
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/farms/areas/?farms={test_farm.id}&tid={test_area['id']}",
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

def test_get_areas(test_farm):
    server_api = get_server_api()

    r = requests.get(
        f"{server_api}{config.API_V1_STR}/farms/areas/?farms={test_farm.id}",
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

def test_update_area(test_farm, test_area):
    server_api = get_server_api()

    # Change area attributes
    test_area['name'] = "Updated name from farmOS-aggregator"
    test_area['description'] = "Update description"
    data = test_area

    response = requests.put(
        f"{server_api}{config.API_V1_STR}/farms/areas/?farms={test_farm.id}",
        json=data,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()

    # Check farm ID included in response
    assert str(test_farm.id) in content

    # Check that the updated area has correct attributes
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/farms/areas/?farms={test_farm.id}&tid={test_area['id']}",
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

def test_delete_area(test_farm, test_area):
    server_api = get_server_api()

    response = requests.delete(
        f"{server_api}{config.API_V1_STR}/farms/areas/?farms={test_farm.id}&id={test_area['id']}",
    )

    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()
