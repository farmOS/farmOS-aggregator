import os

from sqlalchemy.orm import Session
from farmOS import farmOS

from app.core.config import settings
from app import crud
from app.schemas.farm import FarmCreate


def get_test_farm_instance(db: Session):
    """Populates database with a farmOS testing farm
    This creates a farm object in the database with valid credentials
        for the farmOS testing instance.

    Returns: the test_farm object
    """
    # Allow requests over HTTP.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Get oauth tokens from farmOS Client
    farm_client = farmOS(
        hostname=settings.TEST_FARM_URL,
        client_id="farm",
        scope="farm_manager",
        version=2,
    )
    token = farm_client.authorize(
        username=settings.TEST_FARM_USERNAME, password=settings.TEST_FARM_PASSWORD
    )
    assert token is not None
    assert "access_token" in token and "refresh_token" in token

    # Remove existing farm from DB if it has the testing URL
    old_farm = crud.farm.get_by_url(db, farm_url=settings.TEST_FARM_URL)
    if old_farm is not None:
        crud.farm.delete(db, farm_id=old_farm.id)

    # Create test farm
    if settings.TEST_FARM_URL is not None:
        farm_in = FarmCreate(
            farm_name=settings.TEST_FARM_NAME,
            url=settings.TEST_FARM_URL,
            scope="user_access",
            active=True,
            token=token,
        )
    else:
        farm_in = FarmCreate(
            farm_name=settings.TEST_FARM_NAME,
            url="http://localhost",
            scope="user_access",
            active=True,
        )

    test_farm = crud.farm.create(db, farm_in=farm_in)
    return test_farm


def delete_test_farm_instance(db: Session, farm_id):
    """Removes the testing farm from the database"""
    crud.farm.delete(db, farm_id=farm_id)
