from app.core.config import settings
from app import crud
from app.db.session import db_session
from app.schemas.farm import FarmCreate


def get_test_farm_instance():
    """Populates database with a farmOS testing farm
    This creates a farm object in the database with valid credentials
        for the settingsured farmOS testing instance.

    Returns: the test_farm object
    """
    # Remove existing farm from DB if it has the testing URL
    old_farm = crud.farm.get_by_url(db_session, farm_url=settings.TEST_FARM_URL)
    if old_farm is not None:
        crud.farm.delete(db_session, farm_id=old_farm.id)

    # Create test farm
    if settings.TEST_FARM_URL is not None:
        farm_in = FarmCreate(
            farm_name=settings.TEST_FARM_NAME,
            url=settings.TEST_FARM_URL,
            scope="user_access",
            active=True
        )
    else:
        farm_in = FarmCreate(
            farm_name=settings.TEST_FARM_NAME,
            url="http://localhost",
            scope="user_access",
            active=True
        )

    test_farm = crud.farm.create(db_session, farm_in=farm_in)
    return test_farm


def delete_test_farm_instance(farm_id):
    """Removes the testing farm from the database"""
    crud.farm.delete(db_session, farm_id=farm_id)