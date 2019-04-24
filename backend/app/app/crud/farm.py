from typing import List, Optional

from sqlalchemy.orm import Session

from app.db_models.farm import Farm
from app.models.farm import FarmCreate

def get_by_id(db_session: Session, *, farm_id: int):
    return db_session.query(Farm).filter(Farm.id == farm_id).first()

def get_by_multi_id(db_session: Session, *, farm_id_list: List[int]):
    return db_session.query(Farm).filter(Farm.id.in_((farm_id_list))).all()

def get_by_url(db_session: Session, *, farm_url: str):
    return db_session.query(Farm).filter(Farm.url == farm_url).first()

def get_multi(db_session: Session, *, skip=0, limit=100) -> List[Optional[Farm]]:
    return db_session.query(Farm).offset(skip).limit(limit).all()

def create(db_session: Session, *, farm_in: FarmCreate) -> Farm:
    farm = Farm(
        farm_name=farm_in.farm_name,
        url=farm_in.url,
        username=farm_in.username,
        password=farm_in.password
    )
    db_session.add(farm)
    db_session.commit()
    db_session.refresh(farm)
    return farm

def delete(db_session: Session, *, farm_id: int):
    farm = get_by_id(db_session=db_session, farm_id=farm_id)
    db_session.delete(farm)
    db_session.commit()

def is_authenticated(Farm):
    return farm.is_authenticated
