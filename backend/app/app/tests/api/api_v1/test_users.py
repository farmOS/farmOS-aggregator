from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.tests.utils.user import user_authentication_headers
from app.tests.utils.utils import random_lower_string


def test_get_users_superuser_me(client: TestClient, superuser_token_headers):
    r = client.get(
        f"{settings.API_V1_PREFIX}/users/me", headers=superuser_token_headers
    )
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_create_user_new_email(client: TestClient, db: Session, superuser_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_PREFIX}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_email(db, email=username)
    assert user.email == created_user["email"]


def test_get_existing_user(client: TestClient, db: Session, superuser_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db, user_in=user_in)
    user_id = user.id
    r = client.get(
        f"{settings.API_V1_PREFIX}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    user = crud.user.get_by_email(db, email=username)
    assert user.email == api_user["email"]


def test_create_user_existing_username(client: TestClient, db: Session, superuser_token_headers):
    username = random_lower_string()
    # username = email
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db, user_in=user_in)
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_PREFIX}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_create_user_by_normal_user(client: TestClient, db: Session):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db, user_in=user_in)
    user_token_headers = user_authentication_headers(client, username, password)
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_PREFIX}/users/", headers=user_token_headers, json=data
    )
    assert r.status_code == 400


def test_retrieve_users(client: TestClient, db: Session, superuser_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db, user_in=user_in)

    username2 = random_lower_string()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    user2 = crud.user.create(db, user_in=user_in2)

    r = client.get(
        f"{settings.API_V1_PREFIX}/users/", headers=superuser_token_headers
    )
    all_users = r.json()

    assert len(all_users) > 1
    for user in all_users:
        assert "email" in user
