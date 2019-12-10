from urllib.parse import urlparse, parse_qs

import requests
import pytest

from app.core import config
from app.models.farm_token import FarmAuthorizationParams
from app.tests.utils.utils import get_server_api, random_lower_string, get_scope_token_headers
from app.api.utils.security import _validate_token


@pytest.fixture
def farm_authorize_headers():
    return get_scope_token_headers("farm:authorize")


def test_authorize_farm(test_farm, farm_authorize_headers):
    server_api = get_server_api()

    data = FarmAuthorizationParams(
        grant_type="authorization_code",
        code=random_lower_string(),
        state=random_lower_string(),
        client_id="farmos_api_client",
    )

    r = requests.post(
        f"{server_api}{config.API_V1_STR}/utils/authorize-farm/{test_farm.id}",
        headers=farm_authorize_headers,
        json=data.dict(),
    )
    # This request should return 200, but no token will be created.
    # This is because we cannot write an integration test for the OAuth Auth code flow at this time.
    assert 200 <= r.status_code < 300

    '''
    # Values to test if we could write an integration test.
    token = r.json()

    db_token = crud.farm_token.get_by_id(db_session, farm_id=test_farm.id)

    assert db_token.farm_id == token.farm_id == test_farm.id
    assert db_token.access_token == token.access_token
    assert db_token.expires_in == token.expires_in
    assert db_token.refresh_token == token.refresh_token
    assert db_token.expires_at == token.expires_at
    '''


def test_farm_authorize_oauth_scope(test_farm):
    server_api = get_server_api()

    r = requests.post(f"{server_api}{config.API_V1_STR}/utils/authorize-farm/{test_farm.id}")
    assert r.status_code == 401


def test_get_farm_auth_link(test_farm, superuser_token_headers):
    server_api = get_server_api()
    server_host = config.SERVER_HOST

    r = requests.post(
        f"{server_api}{config.API_V1_STR}/utils/farm-auth-link/{test_farm.id}",
        headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    assert r.json() is not None

    # Check the returned farm authorization link
    link = urlparse(r.json())
    assert link.scheme is not None

    # Cannot assert netloc == server_host because it is defined in an environment variable
    # that is not set in the backend-tests container
    # assert link.netloc == server_host
    assert link.netloc is not ''

    # Check that the path includes the correct farm ID
    assert link.path == f"/authorize-farm/{test_farm.id}"

    # Check that an api_token query param is included
    assert link.query is not None
    params = parse_qs(link.query)
    assert 'api_token' in params
    token = params['api_token'][0]

    # Validate the api_token
    token_data = _validate_token(token)
    assert token_data is not None
    assert token_data.farm_id == [test_farm.id]
    assert token_data.scopes is not None
    assert len(token_data.scopes) > 0

    # Test that the api_token has access to read /api/v1/farms/{id}
    r = requests.get(
        f"{server_api}{config.API_V1_STR}/farms/{test_farm.id}",
        headers={'api_token': token},
    )
    assert 200 <= r.status_code < 300
    farm_info = r.json()
    assert farm_info['id'] == test_farm.id
    assert farm_info['farm_name'] == test_farm.farm_name

    # Test that the returned link has access to the utils/authorize-farm endpoint
    data = FarmAuthorizationParams(
        grant_type="authorization_code",
        code=random_lower_string(),
        state=random_lower_string(),
        client_id="farmos_api_client",
    )

    r = requests.post(
        f"{server_api}{config.API_V1_STR}/utils/authorize-farm/{test_farm.id}",
        headers={'api_token': token},
        json=data.dict(),
    )
    # This request should return 200, but no token will be created.
    # This is because we cannot write an integration test for the OAuth Auth code flow at this time.
    assert 200 <= r.status_code < 300
