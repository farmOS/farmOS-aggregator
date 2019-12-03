import requests
import pytest

from app.core import config
from app.models.farm_token import FarmAuthorizationParams
from app.tests.utils.utils import get_server_api, random_lower_string, get_scope_token_headers


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
