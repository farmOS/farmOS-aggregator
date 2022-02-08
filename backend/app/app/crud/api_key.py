import logging

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.jwt import create_api_key
from app.models.api_key import ApiKey
from app.schemas.api_key import ApiKeyCreate, ApiKeyUpdate

logger = logging.getLogger(__name__)


def get_by_id(db: Session, key_id: int):
    return db.query(ApiKey).filter(ApiKey.id == key_id).first()


def get_by_key(db: Session, key: bytes):
    return db.query(ApiKey).filter(ApiKey.key == key).first()


def get_multi(db: Session):
    return db.query(ApiKey).all()


def create(db: Session, api_key_in: ApiKeyCreate):
    # Generate the JWT token that will be saved as the 'key'.
    key = create_api_key(
        farm_id=api_key_in.farm_id,
        all_farms=api_key_in.all_farms,
        scopes=api_key_in.scopes,
    )
    db_item = ApiKey(key=key, **api_key_in.dict())
    db.add(db_item)
    db.commit()

    logger.debug("Created API Key: " + key.decode())
    db.refresh(db_item)
    return db_item


def update(db: Session, *, api_key: ApiKey, api_key_in: ApiKeyUpdate):
    api_key_data = jsonable_encoder(api_key)
    update_data = api_key_in.dict(exclude_unset=True)
    for field in api_key_data:
        if field in update_data:
            setattr(api_key, field, update_data[field])
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return api_key


def delete(db: Session, *, key_id: int):
    key = get_by_id(db=db, key_id=key_id)
    db.delete(key)
    db.commit()
