from app import crud
from app.db.session import db_session
from app.models.farm import FarmInCreate
from app.tests.utils.utils import random_lower_string

def test_create_farm():
    farm_name = random_lower_string()
    url = random_lower_string()
    username = random_lower_string()
    password = random_lower_string()
    farm_in = FarmInCreate(
        farm_name=farm_name,
        url=url,
        username=username,
        password=password,
    )
    farm = crud.farm.create(db_session, farm_in=farm_in)
    assert farm.farm_name == farm_name
