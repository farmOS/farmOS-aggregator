import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.tests.utils.utils import farmOS_testing_server, get_scope_token_headers


@pytest.fixture
def farm_logs_headers(client: TestClient):
    return get_scope_token_headers(client=client, scopes="farm:read farm.logs")


@farmOS_testing_server
def test_get_logs(client: TestClient, test_farm, farm_logs_headers):
    r = client.get(
        f"{settings.API_V1_PREFIX}/farms/logs/?farm_id={test_farm.id}",
        headers=farm_logs_headers,
    )
    # Check response
    assert 200 <= r.status_code < 300
    logs = r.json()

    # Check farm ID included in response
    assert str(test_farm.id) in logs

    # Check logs are returned for the farm
    test_farm_logs = logs[str(test_farm.id)]
    assert len(test_farm_logs) > 1
    for log in test_farm_logs:
        assert "type" in log

    assert str(test_farm.id) in logs

    test_farm_logs = logs[str(test_farm.id)]
    assert len(test_farm_logs) > 1
    for log in test_farm_logs:
        assert "type" in log


@farmOS_testing_server
def test_create_log(client: TestClient, test_farm, test_log, farm_logs_headers):
    data = test_log

    response = client.post(
        f"{settings.API_V1_PREFIX}/farms/logs/?farm_id={test_farm.id}",
        headers=farm_logs_headers,
        json=data,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()

    # Check farm ID included in response
    assert str(test_farm.id) in content

    # Check log was created
    test_farm_logs = content[str(test_farm.id)]
    assert len(test_farm_logs) == 1
    assert 'id' in test_farm_logs[0]
    created_log_id = test_farm_logs[0]['id']
    test_log['id'] = created_log_id

    # Check that the created log has correct attributes
    response = client.get(
        f"{settings.API_V1_PREFIX}/farms/logs/?farm_id={test_farm.id}&id={test_log['id']}",
        headers=farm_logs_headers,
        json=data,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()
    assert str(test_farm.id) in content
    assert len(content[str(test_farm.id)]) == 1
    created_log = content[str(test_farm.id)][0]
    # Check attributes
    assert created_log['type'] == data['type']
    # Check that an optional attribute was populated
    assert bool(int(created_log['done'])) == data['done']


@farmOS_testing_server
def test_update_log(client: TestClient, test_farm, test_log, farm_logs_headers):
    # Change log attributes
    test_log['name'] = "Updated name from farmOS-aggregator"
    test_log['done'] = False
    data = test_log

    response = client.put(
        f"{settings.API_V1_PREFIX}/farms/logs/?farm_id={test_farm.id}",
        headers=farm_logs_headers,
        json=data,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()

    # Check farm ID included in response
    assert str(test_farm.id) in content
    assert len(content[str(test_farm.id)]) == 1
    response_log = content[str(test_farm.id)][0]
    assert 'id' in response_log
    assert test_log['id'] == str(response_log['id'])

    # Check that the updated log has correct attributes
    response = client.get(
        f"{settings.API_V1_PREFIX}/farms/logs/?farm_id={test_farm.id}&id={test_log['id']}",
        headers=farm_logs_headers,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()
    assert str(test_farm.id) in content
    assert len(content[str(test_farm.id)]) == 1
    updated_log = content[str(test_farm.id)][0]
    # Check attributes
    assert updated_log['name'] == data['name']
    # Check that an optional attribute was updated
    assert bool(int(updated_log['done'])) == data['done']


@farmOS_testing_server
def test_delete_log(client: TestClient, test_farm, test_log, farm_logs_headers):
    response = client.delete(
        f"{settings.API_V1_PREFIX}/farms/logs/?farm_id={test_farm.id}&id={test_log['id']}",
        headers=farm_logs_headers,
    )

    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()


@farmOS_testing_server
def test_farm_logs_oauth_scope(client: TestClient):
    r = client.get(f"{settings.API_V1_PREFIX}/farms/logs")
    assert r.status_code == 401
