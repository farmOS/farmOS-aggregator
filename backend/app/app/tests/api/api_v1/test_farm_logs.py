import requests

from app import crud
from app.core import config
from app.db.session import db_session
from app.tests.utils.utils import get_server_api, random_lower_string

def test_get_logs(test_farm):
    server_api = get_server_api()

    r = requests.get(
        f"{server_api}{config.API_V1_STR}/farms/logs/?farms={test_farm.id}&page=1",
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

def test_create_log(test_farm, test_log):
    server_api = get_server_api()

    data = test_log

    response = requests.post(
        f"{server_api}{config.API_V1_STR}/farms/logs/?farms={test_farm.id}",
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

    # Check that the creats log has correct attributes
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/farms/logs/?farms={test_farm.id}&id={test_log['id']}",
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

def test_update_log(test_farm, test_log):
    server_api = get_server_api()

    # Change log attributes
    test_log['name'] = "Updated name from farmOS-aggregator"
    test_log['done'] = False
    data = test_log

    response = requests.put(
        f"{server_api}{config.API_V1_STR}/farms/logs/?farms={test_farm.id}",
        json=data,
    )
    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()

    # Check farm ID included in response
    assert str(test_farm.id) in content

    # Check that the updated log has correct attributes
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/farms/logs/?farms={test_farm.id}&id={test_log['id']}",
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

def test_delete_log(test_farm, test_log):
    server_api = get_server_api()

    response = requests.delete(
        f"{server_api}{config.API_V1_STR}/farms/logs/?farms={test_farm.id}&id={test_log['id']}",
    )

    # Check response
    assert 200 <= response.status_code < 300
    content = response.json()
