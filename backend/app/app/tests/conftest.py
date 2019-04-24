import pytest

from app.tests.utils.utils import get_server_api, get_superuser_token_headers
from app.tests.utils.farm import get_test_farm_instance


@pytest.fixture(scope="module")
def server_api():
    return get_server_api()


@pytest.fixture(scope="module")
def superuser_token_headers():
    return get_superuser_token_headers()

@pytest.fixture(scope='module')
def test_farm():
    return get_test_farm_instance()

@pytest.fixture(scope='module')
def test_log():
    data = {
        "name": "Test Log from farmOS-aggregator",
        "type": "farm_observation",
        "done": True
    }

    return data
