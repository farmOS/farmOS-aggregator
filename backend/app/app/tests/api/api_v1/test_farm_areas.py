import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.tests.utils.utils import farmOS_testing_server, get_scope_token_headers


@pytest.fixture
def farm_areas_headers(client: TestClient):
    return get_scope_token_headers(client=client, scopes="farm:read farm.areas")


@pytest.fixture(autouse=True)
def areas_vid(client: TestClient, test_farm, all_scopes_token_headers):
    response = client.get(
        f"{settings.API_V1_PREFIX}/farms/info/?farm_id={test_farm.id}",
        headers=all_scopes_token_headers,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()

    # Check farm ID included in response
    assert str(test_farm.id) in content
    content = content[str(test_farm.id)]

    # Check that farm info includes farm_areas vid
    assert 'info' in content
    assert 'resources' in content['info']
    assert 'taxonomy_term' in content['info']['resources']
    assert 'farm_areas' in content['info']['resources']['taxonomy_term']
    assert 'vid' in content['info']['resources']['taxonomy_term']['farm_areas']

    # Assign AREAS_VID to use the farm_areas vid value in later tests.
    areas_vid = content['info']['resources']['taxonomy_term']['farm_areas']['vid']
    yield areas_vid


@farmOS_testing_server
def test_create_area(client: TestClient, test_farm, test_area, areas_vid, farm_areas_headers):
    data = test_area
    # Update the vid of the farm_areas term.
    data['vocabulary'] = areas_vid
    print(areas_vid)

    response = client.post(
        f"{settings.API_V1_PREFIX}/farms/areas/?farm_id={test_farm.id}",
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
    response = client.get(
        f"{settings.API_V1_PREFIX}/farms/areas/?farm_id={test_farm.id}&tid={test_area['id']}",
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


@farmOS_testing_server
def test_get_areas(client: TestClient, test_farm, farm_areas_headers):
    r = client.get(
        f"{settings.API_V1_PREFIX}/farms/areas/?farm_id={test_farm.id}",
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


@farmOS_testing_server
def test_update_area(client: TestClient, test_farm, test_area, areas_vid, farm_areas_headers):
    # Change area attributes
    test_area['name'] = "Updated name from farmOS-aggregator"
    test_area['description'] = "Update description"

    data = test_area
    # Update the vid of the farm_areas term.
    data['vocabulary'] = areas_vid

    response = client.put(
        f"{settings.API_V1_PREFIX}/farms/areas/?farm_id={test_farm.id}",
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
    response = client.get(
        f"{settings.API_V1_PREFIX}/farms/areas/?farm_id={test_farm.id}&tid={test_area['id']}",
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


@farmOS_testing_server
def test_delete_area(client: TestClient, test_farm, test_area, farm_areas_headers):
    response = client.delete(
        f"{settings.API_V1_PREFIX}/farms/areas/?farm_id={test_farm.id}&id={test_area['id']}",
        headers=farm_areas_headers,
    )

    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()


@farmOS_testing_server
def test_farm_areas_oauth_scope(client: TestClient):
    r = client.get(f"{settings.API_V1_PREFIX}/farms/areas")
    assert r.status_code == 401
