import pytest

from app.tests.utils.utils import get_server_api, get_superuser_token_headers, get_all_scopes_token_headers
from app.tests.utils.farm import get_test_farm_instance, delete_test_farm_instance


@pytest.fixture(scope="module")
def server_api():
    return get_server_api()


@pytest.fixture(scope="module")
def superuser_token_headers():
    return get_superuser_token_headers()

@pytest.fixture(scope="module")
def all_scopes_token_headers():
    return get_all_scopes_token_headers()

@pytest.fixture(scope='package')
def test_farm():
    farm = get_test_farm_instance()
    yield farm

    # Delete the test farm from the DB for cleanup.
    delete_test_farm_instance(farm.id)

@pytest.fixture(scope='module')
def test_log():
    data = {
        "name": "Test Log from farmOS-aggregator",
        "type": "farm_observation",
        "done": True
    }

    return data

@pytest.fixture(scope='module')
def test_asset():
    data = {
        "name": "Test Tractor from farmOS-aggregator",
        "type": "equipment",
        "serial_number": "1234567890"
    }

    return data

@pytest.fixture(scope='module')
def test_term():
    data = {
        "name": "Test crop term from farmOS-aggregator",
        "description": "Description from farmOS-aggregator",
        "vocabulary": 7, # default VID for crops
    }

    return data

@pytest.fixture(scope='module')
def test_area():
    data = {
        "name": "Test farmOS-aggregator field",
        "area_type": "field",
        "description": "Description from farmOS-aggregator",
        "vocabulary": 1, # default VID for areas
    }

    return data
