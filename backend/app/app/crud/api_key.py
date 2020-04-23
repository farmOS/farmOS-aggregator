import logging

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.api_key import ApiKey
from app.schemas.api_key import ApiKeyCreate, ApiKeyUpdate
from app.core.jwt import create_api_key

logger = logging.getLogger(__name__)


def get_by_id(db_session: Session, key_id: int):
    return db_session.query(ApiKey).filter(ApiKey.id == key_id).first()


def get_by_key(db_session: Session, key: bytes):
    return db_session.query(ApiKey).filter(ApiKey.key == key).first()


def get_multi(db_session: Session):
    return db_session.query(ApiKey).all()


def create(db_session: Session, api_key_in: ApiKeyCreate):
    # Generate the JWT token that will be saved as the 'key'.
    key = create_api_key(
        farm_id=api_key_in.farm_id,
        all_farms=api_key_in.all_farms,
        scopes=api_key_in.scopes
    )
    db_item = ApiKey(key=key, **api_key_in.dict())
    db_session.add(db_item)
    db_session.commit()

    logger.debug("Created API Key: " + key.decode())
    db_session.refresh(db_item)
    return db_item


def update(db_session: Session, *, api_key: ApiKey, api_key_in: ApiKeyUpdate):
    api_key_data = jsonable_encoder(api_key)
    update_data = api_key_in.dict(exclude_unset=True)
    for field in api_key_data:
        if field in update_data:
            setattr(api_key, field, update_data[field])
    db_session.add(api_key)
    db_session.commit()
    db_session.refresh(api_key)
    return api_key


def delete(db_session: Session, *, key_id: int):
    key = get_by_id(db_session=db_session, key_id=key_id)
    db_session.delete(key)
    db_session.commit()