from app import crud
from app.core.config import settings

# make sure all SQL Alchemy schemas are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize properly relationships
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.db import base
from app.schemas.user import UserCreate


def init_db(db):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, user_in=user_in)
