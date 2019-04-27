import requests

from app import crud
from app.core import config
from app.db.session import db_session
from app.tests.utils.utils import get_server_api, random_lower_string

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

