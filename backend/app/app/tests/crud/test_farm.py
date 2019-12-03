from app import crud
from app.db.session import db_session
from app.models.farm import FarmCreate
from app.tests.utils.utils import random_lower_string

def test_create_delete_farm():
    farm_name = random_lower_string()
    url = random_lower_string()
    username = random_lower_string()
    password = random_lower_string()
    farm_in = FarmCreate(
        farm_name=farm_name,
        url=url,
        username=username,
        password=password,
    )
    farm = crud.farm.create(db_session, farm_in=farm_in)
    assert farm.farm_name == farm_name
    assert farm.url == url
    assert farm.username == username
    assert farm.password == password

    # Remove farm from DB
    crud.farm.delete(db_session, farm_id=farm.id)
    farm = crud.farm.get_by_id(db_session, farm_id=farm.id)
    assert farm is None

def test_optional_username_password():
    farm_name = random_lower_string()
    url = random_lower_string()
    farm_in = FarmCreate(farm_name=farm_name, url=url)
    farm = crud.farm.create(db_session, farm_in=farm_in)
    assert farm.farm_name == farm_name
    assert farm.url == url
    assert farm.username is None
    assert farm.password is None

    # Remove farm from DB
    crud.farm.delete(db_session, farm_id=farm.id)
    farm = crud.farm.get_by_id(db_session, farm_id=farm.id)
    assert farm is None
