from app.core import config
from app import crud
from app.db.session import db_session
from app.schemas.farm import FarmCreate, FarmUpdate
from app.tests.utils.utils import random_lower_string


def test_create_delete_default_farm_with_token():
    """Leave the active flag unset. Test form correct system default flag."""

    farm_name = random_lower_string()
    url = random_lower_string()

    # Provide a token on creation
    token = {
        'access_token': random_lower_string(),
        'expires_in': random_lower_string(),
        'refresh_token': random_lower_string(),
        'expires_at': random_lower_string(),
    }

    farm_in = FarmCreate(
        farm_name=farm_name,
        url=url,
        scope='user_access',
        token=token,
    )
    farm = crud.farm.create(db_session, farm_in=farm_in)
    assert farm.farm_name == farm_name
    assert farm.url == url

    if config.FARM_ACTIVE_AFTER_REGISTRATION:
        assert farm.active is True
    else:
        assert farm.active is False

    # Test that token was created
    assert farm.token is not None
    assert farm.token.access_token == token['access_token']
    assert farm.token.expires_at == token['expires_at']
    assert farm.token.refresh_token == token['refresh_token']
    assert farm.token.expires_in == token['expires_in']

    # Remove farm from DB
    crud.farm.delete(db_session, farm_id=farm.id)
    farm = crud.farm.get_by_id(db_session, farm_id=farm.id)
    assert farm is None


def test_create_farm_update_token():
    """Update the token after farm is created."""

    farm_name = random_lower_string()
    url = random_lower_string()

    farm_in = FarmCreate(
        farm_name=farm_name,
        scope='user_access',
        url=url,
    )
    farm = crud.farm.create(db_session, farm_in=farm_in)
    assert farm.farm_name == farm_name
    assert farm.url == url
    assert farm.token is None

    if config.FARM_ACTIVE_AFTER_REGISTRATION:
        assert farm.active is True
    else:
        assert farm.active is False

    # Create a new token
    new_token = {
        'access_token': random_lower_string(),
        'expires_in': random_lower_string(),
        'refresh_token': random_lower_string(),
        'expires_at': random_lower_string(),
    }

    farm_update = FarmUpdate(
        token=new_token,
    )
    farm = crud.farm.update(db_session, farm=farm, farm_in=farm_update)
    assert farm.farm_name == farm_name
    assert farm.url == url

    # Test that token was created
    assert farm.token is not None
    assert farm.token.access_token == new_token['access_token']
    assert farm.token.expires_at == new_token['expires_at']
    assert farm.token.refresh_token == new_token['refresh_token']
    assert farm.token.expires_in == new_token['expires_in']

    # Create a new token
    new_token = {
        'access_token': '',
        'expires_in': '',
        'refresh_token': '',
        'expires_at': '',
    }

    farm_update = FarmUpdate(
        token=new_token,
    )
    farm = crud.farm.update(db_session, farm=farm, farm_in=farm_update)
    assert farm.farm_name == farm_name
    assert farm.url == url

    # Test that token was created
    assert farm.token is not None
    assert farm.token.access_token == new_token['access_token']
    assert farm.token.expires_at == new_token['expires_at']
    assert farm.token.refresh_token == new_token['refresh_token']
    assert farm.token.expires_in == new_token['expires_in']

    # Remove farm from DB
    crud.farm.delete(db_session, farm_id=farm.id)
    farm = crud.farm.get_by_id(db_session, farm_id=farm.id)
    assert farm is None


def test_create_farm_cant_delete_token():
    """Ensure that the token cannot be removed when None is supplied."""

    farm_name = random_lower_string()
    url = random_lower_string()

    # Provide a token on creation
    token = {
        'access_token': random_lower_string(),
        'expires_in': random_lower_string(),
        'refresh_token': random_lower_string(),
        'expires_at': random_lower_string(),
    }

    farm_in = FarmCreate(
        farm_name=farm_name,
        url=url,
        scope='user_access',
        token=token,
    )
    farm = crud.farm.create(db_session, farm_in=farm_in)
    assert farm.farm_name == farm_name
    assert farm.url == url

    if config.FARM_ACTIVE_AFTER_REGISTRATION:
        assert farm.active is True
    else:
        assert farm.active is False

    # Test that token was created
    assert farm.token is not None
    assert farm.token.access_token == token['access_token']
    assert farm.token.expires_at == token['expires_at']
    assert farm.token.refresh_token == token['refresh_token']
    assert farm.token.expires_in == token['expires_in']

    farm_update = FarmUpdate(
        token=None,
    )
    farm = crud.farm.update(db_session, farm=farm, farm_in=farm_update)
    assert farm.farm_name == farm_name
    assert farm.url == url

    # Check that the token is unchanged.
    assert farm.token is not None
    assert farm.token.access_token == token['access_token']
    assert farm.token.expires_at == token['expires_at']
    assert farm.token.refresh_token == token['refresh_token']
    assert farm.token.expires_in == token['expires_in']

    # Remove farm from DB
    crud.farm.delete(db_session, farm_id=farm.id)
    farm = crud.farm.get_by_id(db_session, farm_id=farm.id)
    assert farm is None


def test_create_delete_active_farm():
    """Configure the active flag to True."""

    farm_name = random_lower_string()
    url = random_lower_string()
    farm_in = FarmCreate(
        farm_name=farm_name,
        url=url,
        scope='user_access',
        active=True,
    )
    farm = crud.farm.create(db_session, farm_in=farm_in)
    assert farm.farm_name == farm_name
    assert farm.url == url
    assert farm.active is True

    # Remove farm from DB
    crud.farm.delete(db_session, farm_id=farm.id)
    farm = crud.farm.get_by_id(db_session, farm_id=farm.id)
    assert farm is None


def test_create_delete_inactive_farm():
    """Configure the active flag to False."""

    farm_name = random_lower_string()
    url = random_lower_string()
    farm_in = FarmCreate(
        farm_name=farm_name,
        url=url,
        scope='user_access',
        active=False,
    )
    farm = crud.farm.create(db_session, farm_in=farm_in)
    assert farm.farm_name == farm_name
    assert farm.url == url
    assert farm.active is False

    # Remove farm from DB
    crud.farm.delete(db_session, farm_id=farm.id)
    farm = crud.farm.get_by_id(db_session, farm_id=farm.id)
    assert farm is None
