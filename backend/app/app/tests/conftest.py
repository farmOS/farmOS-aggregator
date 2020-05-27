from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.session import SessionLocal
from app.tests.utils.utils import get_superuser_token_headers, get_all_scopes_token_headers
from app.tests.utils.farm import get_test_farm_instance, delete_test_farm_instance


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient):
    return get_superuser_token_headers(client=client)


@pytest.fixture(scope="module")
def all_scopes_token_headers():
    return get_all_scopes_token_headers(client=client)


@pytest.fixture(scope='package')
def test_farm():
    db = SessionLocal()
    farm = get_test_farm_instance(db)
    yield farm

    # Delete the test farm from the DB for cleanup.
    delete_test_farm_instance(db, farm.id)


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
