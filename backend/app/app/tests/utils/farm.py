import farmOS

from app.core import config
from app import crud
from app.db.session import db_session
from app.models.farm import FarmCreate


def get_test_farm_instance():
    """Populates database with a farmOS testing farm
    This creates a farm object in the database with valid credentials
        for the configured farmOS testing instance.

    Returns: the test_farm object
    """
    # Remove existing farm from DB if it has the testing URL
    old_farm = crud.farm.get_by_url(db_session, farm_url=config.TEST_FARM_URL)
    if old_farm is not None:
        crud.farm.delete(db_session, farm_id=old_farm.id)

    # Create test farm
    if config.has_valid_test_configuration():
        farm_in = FarmCreate(
            farm_name=config.TEST_FARM_NAME,
            url=config.TEST_FARM_URL,
            username=config.TEST_FARM_USERNAME,
            password=config.TEST_FARM_PASSWORD,
        )
    else:
        farm_in = FarmCreate(
            farm_name=config.TEST_FARM_NAME,
            url="http://localhost",
            username="username",
            password="password",
        )

    test_farm = crud.farm.create(db_session, farm_in=farm_in)
    return test_farm


def delete_test_farm_instance(farm_id):
    """Removes the testing farm from the database"""
    crud.farm.delete(db_session, farm_id=farm_id)