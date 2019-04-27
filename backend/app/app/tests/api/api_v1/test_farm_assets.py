import requests

from app import crud
from app.core import config
from app.db.session import db_session
from app.tests.utils.utils import get_server_api, random_lower_string

def test_get_assets(test_farm):
    server_api = get_server_api()

    r = requests.get(
        f"{server_api}{config.API_V1_STR}/farms/assets/?farms={test_farm.id}",
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

