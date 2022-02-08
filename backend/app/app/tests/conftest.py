from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.db.session import SessionLocal
from app.main import app
from app.tests.utils.farm import delete_test_farm_instance, get_test_farm_instance
from app.tests.utils.utils import (
    get_all_scopes_token_headers,
    get_superuser_token_headers,
)


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


@pytest.fixture(scope="package")
def test_farm():
    db = SessionLocal()
    farm = get_test_farm_instance(db)
    yield farm

    # Delete the test farm from the DB for cleanup.
    delete_test_farm_instance(db, farm.id)


@pytest.fixture(scope="module")
def test_log():
    data = {
        "type": "activity",
        "attributes": {
            "name": "Test Log from farmOS-aggregator",
            "status": "done",
        },
    }

    return data
