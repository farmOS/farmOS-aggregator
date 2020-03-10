import random
import string

import requests
import pytest

from app.core.config import settings
from app.schemas.api_key import ApiKeyCreate


farmOS_testing_server = pytest.mark.skipif(
    settings.TEST_FARM_URL is None,
    reason="farmOS Testing Server not configured. Skipping farmOS test server integration tests.",
)


def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))


def get_server_api():
    server_name = f"http://{settings.SERVER_NAME}"
    return server_name


def get_superuser_token_headers():
    server_api = get_server_api()
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/login/access-token", data=login_data
    )
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    # superuser_token_headers = headers
    return headers


def get_all_scopes_token_headers():
    return _create_headers_with_scopes("farm:create farm:read farm:update farm:delete farm:authorize farm.info farm.logs farm.assets farm.terms farm.areas")


def get_scope_token_headers(scopes):
    return _create_headers_with_scopes(scopes)


def _create_headers_with_scopes(scopes):
    server_api = get_server_api()
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
        "scope": scopes,
    }
    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/login/access-token", data=login_data
    )
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def get_api_key_headers(api_key_params: ApiKeyCreate):
    server_api = get_server_api()
    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/api-keys",
        headers=get_superuser_token_headers(),
        data=api_key_params.json()
    )
    api_key = r.json()
    key = api_key["key"]
    headers = {"api-key": f"{key}"}
    return headers
