import logging
from typing import List, Optional
import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core import config
from app.db_models.farm import Farm
from app.models.farm import FarmCreate, FarmUpdate
from app.db_models.farm_token import FarmToken
from app.models.farm_info import FarmInfo


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler)


def get_by_id(db_session: Session, *, farm_id: int):
    return db_session.query(Farm).filter(Farm.id == farm_id).first()

def get_by_multi_id(db_session: Session, *, farm_id_list: List[int]):
    return db_session.query(Farm).filter(Farm.id.in_((farm_id_list))).all()

def get_by_url(db_session: Session, *, farm_url: str):
    return db_session.query(Farm).filter(Farm.url == farm_url).first()

def get_multi(db_session: Session, *, skip=0, limit=100) -> List[Optional[Farm]]:
    return db_session.query(Farm).offset(skip).limit(limit).all()

def create(db_session: Session, *, farm_in: FarmCreate) -> Farm:
    logging.debug(f"Adding new farm: {farm_in.farm_name}")
    # Disable new farm profiles by default.
    active = False

    # If the active attribute is assigned, use it.
    if farm_in.active is not None:
        logging.debug(f"New farm provided 'active = {farm_in.active}'")
        active = farm_in.active
    # Enable farm profile if configured and not overridden above.
    elif config.FARM_ACTIVE_AFTER_REGISTRATION:
        logging.debug(f"FARM_ACTIVE_AFTER_REGISTRATION is enabled. New farm will be active.")
        active = True

    farm = Farm(
        farm_name=farm_in.farm_name,
        url=farm_in.url,
        username=farm_in.username,
        password=farm_in.password,
        notes=farm_in.notes,
        tags=farm_in.tags,
        info=farm_in.info,
        active=active,
    )
    db_session.add(farm)
    db_session.commit()
    db_session.refresh(farm)

    if farm_in.token is not None:
        logging.debug("Saving provided token with new farm profile.")
        new_token = FarmToken(farm_id=farm.id, **farm_in.token.dict())
        db_session.add(new_token)
        db_session.commit()
        db_session.refresh(new_token)

    db_session.refresh(farm)
    return farm

def update(db_session: Session, *, farm: Farm, farm_in: FarmUpdate):
    farm_data = jsonable_encoder(farm)
    update_data = farm_in.dict(skip_defaults=True)
    for field in farm_data:
        if field in update_data:
            setattr(farm, field, update_data[field])
    db_session.add(farm)
    db_session.commit()
    db_session.refresh(farm)
    return farm

def update_info(db_session: Session, *, farm: Farm, info: FarmInfo):
    setattr(farm, 'info', info)
    db_session.add(farm)
    db_session.commit()
    db_session.refresh(farm)
    return farm

def delete(db_session: Session, *, farm_id: int):
    farm = get_by_id(db_session=db_session, farm_id=farm_id)
    db_session.delete(farm)
    db_session.commit()

def update_last_accessed(db_session: Session, *, farm_id: int):
    farm = get_by_id(db_session=db_session, farm_id=farm_id)
    setattr(farm, "last_accessed", datetime.datetime.now())
    db_session.add(farm)
    db_session.commit()
    db_session.refresh(farm)
    return farm

def update_is_authorized(db_session: Session, *, farm_id: int, is_authorized: bool):
    farm = get_by_id(db_session=db_session, farm_id=farm_id)
    setattr(farm, "is_authorized", is_authorized)
    db_session.add(farm)
    db_session.commit()
    db_session.refresh(farm)
    return farm

def is_authenticated(Farm):
    return farm.is_authenticated
