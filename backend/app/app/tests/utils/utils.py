import random
import string

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.schemas.api_key import ApiKeyCreate


farmOS_testing_server = pytest.mark.skipif(
    settings.TEST_FARM_URL is None,
    reason="farmOS Testing Server not configured. Skipping farmOS test server integration tests.",
)


def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))


def get_superuser_token_headers(client: TestClient):
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(
        f"{settings.API_V2_PREFIX}/login/access-token", data=login_data
    )
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    # superuser_token_headers = headers
    return headers


def get_all_scopes_token_headers(client: TestClient):
    return _create_headers_with_scopes(client=client, scopes="farm:create farm:read farm:update farm:delete farm:authorize farm.info farm.logs farm.assets farm.terms farm.areas")


def get_scope_token_headers(client: TestClient, scopes):
    return _create_headers_with_scopes(client, scopes)


def _create_headers_with_scopes(client: TestClient, scopes):
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
        "scope": scopes,
    }
    r = client.post(
        f"{settings.API_V2_PREFIX}/login/access-token", data=login_data
    )
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def get_api_key_headers(client: TestClient, api_key_params: ApiKeyCreate):
    r = client.post(
        f"{settings.API_V2_PREFIX}/api-keys/",
        headers=get_superuser_token_headers(client=client),
        data=api_key_params.json()
    )
    api_key = r.json()
    key = api_key["key"]
    headers = {"api-key": f"{key}"}
    return headers
