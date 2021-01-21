from app.core.jwt import create_farm_api_token
from app.routers.utils.security import _validate_token


def test_create_api_token():
    farm_id_list = [1, 2, 3]
    scopes = ["scope1", "scope2"]

    token = create_farm_api_token(farm_id_list, scopes)
    assert token is not None

    token_data = _validate_token(token)
    assert token_data is not None

    # api_tokens are not associated with a user.
    assert token_data.user_id is None

    # Check that farm_id and scopes match.
    assert token_data.farm_id == farm_id_list
    assert token_data.scopes == scopes
