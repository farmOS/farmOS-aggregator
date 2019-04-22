import requests

from app import crud
from app.core import config
from app.db.session import db_session
from app.models.farm import FarmInCreate
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
