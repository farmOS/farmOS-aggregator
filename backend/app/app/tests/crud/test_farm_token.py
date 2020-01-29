from app.crud import farm_token
from app.db.session import db_session
from app.schemas.farm_token import FarmTokenCreate, FarmTokenUpdate
from app.tests.utils.utils import random_lower_string

def test_create_farm_token(test_farm):
    token = FarmTokenCreate(
        farm_id=test_farm.id,
        access_token=random_lower_string(),
        expires_in=random_lower_string(),
        refresh_token=random_lower_string(),
        expires_at=random_lower_string()
    )

    # Check for existing token
    old_token = farm_token.get_farm_token(db_session, test_farm.id)
    if old_token is None:
        farm_token.create_farm_token(db_session, token=token)
    else:
        farm_token.update_farm_token(db_session, token=old_token, token_in=token)

    db_token = farm_token.get_farm_token(db_session, farm_id=test_farm.id)

    assert db_token.farm_id == token.farm_id == test_farm.id
    assert db_token.access_token == token.access_token
    assert db_token.expires_in == token.expires_in
    assert db_token.refresh_token == token.refresh_token
    assert db_token.expires_at == token.expires_at

def test_update_farm_token(test_farm):
    db_token = farm_token.get_farm_token(db_session, farm_id=test_farm.id)
    assert db_token is not None
    assert db_token.farm_id == test_farm.id

    token_changes = FarmTokenUpdate(
        id=db_token.id,
        farm_id=db_token.farm_id,
        access_token=None,
        expires_in=None,
        refresh_token=None,
        expires_at=None
    )
    new_token = farm_token.update_farm_token(db_session, token=db_token, token_in=token_changes)
    assert new_token.id == db_token.id
    assert new_token.farm_id == db_token.farm_id == test_farm.id

    # Check that the farm_token was reset.
    assert new_token.access_token is None
    assert new_token.expires_in is None
    assert new_token.refresh_token is None
    assert new_token.expires_at is None
