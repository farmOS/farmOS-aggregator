from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models.farm_token import FarmToken
from app.schemas.farm_token import FarmTokenCreate, FarmTokenBase


def get_farm_token(db: Session, farm_id: int):
    return db.query(FarmToken).filter(FarmToken.farm_id == farm_id).first()


def create_farm_token(db: Session, token: FarmTokenCreate):
    db_item = FarmToken(**token.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_farm_token(db: Session, token: FarmToken, token_in: FarmTokenBase):
    token_data = jsonable_encoder(token)
    update_data = token_in.dict(exclude_unset=True)
    for field in token_data:
        if field in update_data:
            setattr(token, field, update_data[field])
    db.add(token)
    db.commit()
    db.refresh(token)
    return token




