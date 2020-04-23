from fastapi.testclient import TestClient

from app import crud
from app.core.config import settings
from app.db.session import db_session
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_lower_string


def user_authentication_headers(client: TestClient, email, password):
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user():
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = crud.user.create(db_session=db_session, user_in=user_in)
    return user
