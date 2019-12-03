import farmOS

from app import crud
from app.db.session import db_session
from app.models.farm import FarmCreate

from .test_farm_credentials import test_farm_credentials

def get_test_farm_credentials():
    return test_farm_credentials

def get_test_farm_instance():
    """Populates database with a farmOS testing farm
    This creates a farm object in the database with valid credentials
        for the configured farmOS testing instance.

    Returns: the test_farm object
    """
    farm_in = FarmCreate(**test_farm_credentials)
    test_farm = crud.farm.create(db_session, farm_in=farm_in)
    return test_farm


def delete_test_farm_instance(farm_id):
    """Removes the testing farm from the database"""
    crud.farm.delete(db_session, farm_id=farm_id)