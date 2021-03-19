from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_lower_string


def test_create_user(db: Session):
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, user_in=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_authenticate_user(db: Session):
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, user_in=user_in)
    authenticated_user = crud.user.authenticate(db, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(db: Session):
    email = random_lower_string()
    password = random_lower_string()
    user = crud.user.authenticate(db, email=email, password=password)
    assert user is None


def test_check_if_user_is_active(db: Session):
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, user_in=user_in)
    is_active = crud.user.is_active(user)
    assert is_active is True


def test_check_if_user_is_active_inactive(db: Session):
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, disabled=True)
    print(user_in)
    user = crud.user.create(db, user_in=user_in)
    print(user)
    is_active = crud.user.is_active(user)
    print(is_active)
    assert is_active


def test_check_if_user_is_superuser(db: Session):
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = crud.user.create(db, user_in=user_in)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is True


def test_check_if_user_is_superuser_normal_user(db: Session):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db, user_in=user_in)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is False


def test_get_user(db: Session):
    password = random_lower_string()
    username = random_lower_string()
    user_in = UserCreate(email=username, password=password, is_superuser=True)
    user = crud.user.create(db, user_in=user_in)
    user_2 = crud.user.get(db, user_id=user.id)
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)
