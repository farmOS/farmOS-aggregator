import logging
from typing import List, Optional
import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.models.farm import Farm
from app.schemas.farm import FarmCreate, FarmUpdate
from app.models.farm_token import FarmToken
from app.schemas.farm_token import FarmTokenCreate
from app.schemas.farm_info import FarmInfo


logger = logging.getLogger(__name__)


def get_by_id(db_session: Session, *, farm_id: int, active: bool = None):
    if active is not None:
        return db_session.query(Farm).filter(Farm.active.is_(active)).filter(Farm.id == farm_id).first()
    else:
        return db_session.query(Farm).filter(Farm.id == farm_id).first()


def get_by_multi_id(db_session: Session, *, farm_id_list: List[int], active: bool = None):
    if active is not None:
        return db_session.query(Farm).filter(Farm.active.is_(active)).filter(Farm.id.in_(farm_id_list)).all()
    else:
        return db_session.query(Farm).filter(Farm.id.in_(farm_id_list)).all()


def get_by_url(db_session: Session, *, farm_url: str, active: bool = None):
    if active is not None:
        return db_session.query(Farm).filter(Farm.active.is_(active)).filter(Farm.url == farm_url).first()
    else:
        return db_session.query(Farm).filter(Farm.url == farm_url).first()


def get_multi(db_session: Session, *, skip=0, limit=100, active: bool = None) -> List[Optional[Farm]]:
    if active is not None:
        return db_session.query(Farm).filter(Farm.active.is_(active)).offset(skip).limit(limit).all()
    else:
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
    elif settings.FARM_ACTIVE_AFTER_REGISTRATION:
        logging.debug(f"FARM_ACTIVE_AFTER_REGISTRATION is enabled. New farm will be active.")
        active = True

    farm = Farm(
        farm_name=farm_in.farm_name,
        url=farm_in.url,
        notes=farm_in.notes,
        tags=farm_in.tags,
        scope=farm_in.scope,
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
    # If provided, handle the token update first.
    if farm_in.token is not None:
        # Check for existing token.
        old_token = crud.farm_token.get_farm_token(db_session, farm.id)

        # Create new token if none existing.
        if old_token is None:
            new_token = FarmTokenCreate(farm_id=farm.id, **farm_in.token.dict())
            token = crud.farm_token.create_farm_token(db_session, token=new_token)
        # Update existing token.
        else:
            token = crud.farm_token.update_farm_token(db_session, token=old_token, token_in=farm_in.token)

    # Prevent deleting token
    del farm_in.token

    farm_data = jsonable_encoder(farm)
    update_data = farm_in.dict(exclude_unset=True)
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


def update_is_authorized(db_session: Session, *, farm_id: int, is_authorized: bool, auth_error: str = None):
    farm = get_by_id(db_session=db_session, farm_id=farm_id)
    setattr(farm, "is_authorized", is_authorized)
    setattr(farm, "auth_error", auth_error)
    db_session.add(farm)
    db_session.commit()
    db_session.refresh(farm)
    return farm


def is_authenticated(farm):
    return farm.is_authenticated
