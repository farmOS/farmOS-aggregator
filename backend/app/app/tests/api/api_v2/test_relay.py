import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.tests.utils.utils import farmOS_testing_server, get_scope_token_headers


@pytest.fixture
def farm_logs_headers(client: TestClient):
    headers = get_scope_token_headers(client=client, scopes="farm:read")
    headers["Content-Type"] = "application/vnd.api+json"
    return headers


@farmOS_testing_server
def test_relay_crud_activity_logs(
    client: TestClient, test_farm, test_log, farm_logs_headers
):
    # Create a log.
    response = client.post(
        f"{settings.API_V2_PREFIX}/farms/relay/api/log/activity?farm_id={test_farm.id}",
        headers=farm_logs_headers,
        json={"data": test_log},
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()
    assert "data" in content

    # Check log was created
    test_farm_log = content["data"]
    assert "id" in test_farm_log
    created_log_id = test_farm_log["id"]
    test_log["id"] = created_log_id

    # Test a GET with the log ID.
    response = client.get(
        f"{settings.API_V2_PREFIX}/farms/relay/api/log/activity/{test_log['id']}?farm_id={test_farm.id}",
        headers=farm_logs_headers,
        json=test_log,
    )

    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()
    assert "data" in content

    # Check attributes
    created_log = content["data"]
    assert created_log["type"] == f"log--{test_log['type']}"
    assert created_log["attributes"]["name"] == test_log["attributes"]["name"]

    # Change log attributes
    test_log["attributes"]["name"] = "Updated name from farmOS-aggregator"
    test_log["attributes"]["status"] = "pending"
    test_log = test_log
    response = client.patch(
        f"{settings.API_V2_PREFIX}/farms/relay/api/log/activity/{test_log['id']}?farm_id={test_farm.id}",
        headers=farm_logs_headers,
        json={"data": test_log},
    )

    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()
    assert "data" in content

    # Check attributes
    updated_log = content["data"]
    assert updated_log["attributes"]["name"] == test_log["attributes"]["name"]

    response = client.delete(
        f"{settings.API_V2_PREFIX}/farms/relay/api/log/activity/{test_log['id']}?farm_id={test_farm.id}",
        headers=farm_logs_headers,
    )
    # Check response
    assert response.status_code == 204


@farmOS_testing_server
def test_farm_resources_permission(client: TestClient):
    r = client.get(f"{settings.API_V2_PREFIX}/farms/resources/logs/activity")
    assert r.status_code == 401
