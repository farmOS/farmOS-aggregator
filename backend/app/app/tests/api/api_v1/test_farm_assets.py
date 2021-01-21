import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.tests.utils.utils import farmOS_testing_server, get_scope_token_headers


@pytest.fixture
def farm_assets_headers(client: TestClient):
    return get_scope_token_headers(client=client, scopes="farm:read farm.assets")


@farmOS_testing_server
def test_create_asset(client: TestClient, test_farm, test_asset, farm_assets_headers):
    data = test_asset

    response = client.post(
        f"{settings.API_V1_PREFIX}/farms/assets/?farm_id={test_farm.id}",
        headers=farm_assets_headers,
        json=data,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()

    # Check farm ID included in response
    assert str(test_farm.id) in content

    # Check asset was created
    test_farm_assets = content[str(test_farm.id)]
    assert len(test_farm_assets) == 1
    assert 'id' in test_farm_assets[0]
    created_asset_id = test_farm_assets[0]['id']
    test_asset['id'] = created_asset_id

    # Check that the creats asset has correct attributes
    response = client.get(
        f"{settings.API_V1_PREFIX}/farms/assets/?farm_id={test_farm.id}&id={test_asset['id']}",
        headers=farm_assets_headers,
        json=data,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()
    assert str(test_farm.id) in content
    assert len(content[str(test_farm.id)]) == 1
    created_asset = content[str(test_farm.id)][0]
    # Check attributes
    assert created_asset['type'] == data['type']
    # Check that an optional attribute was populated
    assert created_asset['serial_number'] == data['serial_number']


@farmOS_testing_server
def test_get_assets(client: TestClient, test_farm, farm_assets_headers):
    r = client.get(
        f"{settings.API_V1_PREFIX}/farms/assets/?farm_id={test_farm.id}",
        headers=farm_assets_headers,
    )
    # Check response
    assert 200 <= r.status_code < 300
    assets = r.json()

    # Check farm ID included in response
    assert str(test_farm.id) in assets

    # Check assets are returned for the farm
    test_farm_assets = assets[str(test_farm.id)]
    assert len(test_farm_assets) > 1
    for asset in test_farm_assets:
        assert "type" in asset

    assert str(test_farm.id) in assets

    test_farm_assets = assets[str(test_farm.id)]
    assert len(test_farm_assets) > 1
    for asset in test_farm_assets:
        assert "type" in asset


@farmOS_testing_server
def test_update_asset(client: TestClient, test_farm, test_asset, farm_assets_headers):
    # Change asset attributes
    test_asset['name'] = "Updated name from farmOS-aggregator"
    test_asset['serial_number'] = 0
    data = test_asset

    response = client.put(
        f"{settings.API_V1_PREFIX}/farms/assets/?farm_id={test_farm.id}",
        headers=farm_assets_headers,
        json=data,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()

    # Check farm ID included in response
    assert str(test_farm.id) in content
    assert len(content[str(test_farm.id)]) == 1
    response_asset = content[str(test_farm.id)][0]
    assert 'id' in response_asset
    assert test_asset['id'] == str(response_asset['id'])

    # Check that the updated asset has correct attributes
    response = client.get(
        f"{settings.API_V1_PREFIX}/farms/assets/?farm_id={test_farm.id}&id={test_asset['id']}",
        headers=farm_assets_headers,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()
    assert str(test_farm.id) in content
    assert len(content[str(test_farm.id)]) == 1
    updated_asset = content[str(test_farm.id)][0]
    # Check attributes
    assert updated_asset['name'] == data['name']
    # Check that an optional attribute was updated
    assert int(updated_asset['serial_number']) == data['serial_number']


@farmOS_testing_server
def test_delete_asset(client: TestClient, test_farm, test_asset, farm_assets_headers):
    response = client.delete(
        f"{settings.API_V1_PREFIX}/farms/assets/?farm_id={test_farm.id}&id={test_asset['id']}",
        headers=farm_assets_headers,
    )

    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()


@farmOS_testing_server
def test_farm_assets_oauth_scope(client: TestClient):
    r = client.get(f"{settings.API_V1_PREFIX}/farms/assets")
    assert r.status_code == 401
