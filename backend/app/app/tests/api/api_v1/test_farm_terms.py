import requests

from app import crud
from app.core import config
from app.db.session import db_session
from app.tests.utils.utils import get_server_api, random_lower_string

def test_get_terms(test_farm):
    server_api = get_server_api()

    r = requests.get(
        f"{server_api}{config.API_V1_STR}/farms/terms/?farms={test_farm.id}",
    )
    # Check response
    assert 200 <= r.status_code < 300
    terms = r.json()

    # Check farm ID included in response
    assert str(test_farm.id) in terms

    # Check terms are returned for the farm
    test_farm_terms = terms[str(test_farm.id)]
    assert len(test_farm_terms) > 1
    for term in test_farm_terms:
        assert "name" in term

    assert str(test_farm.id) in terms

    test_farm_terms = terms[str(test_farm.id)]
    assert len(test_farm_terms) > 1
    for term in test_farm_terms:
        assert "name" in term

