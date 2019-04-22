from typing import List, Optional

from app.db_models.farm import Farm
from app.models.farm import FarmInCreate

def get_by_id(db_session, *, farm_id: int):
    return db_session.query(Farm).filter(Farm.id == farm_id).first()

def get_by_multi_id(db_session, *, farm_id_list: List[int]):
    return db_session.query(Farm).filter(Farm.id.in_((farm_id_list))).all()

def get_by_url(db_session, *, farm_url: str):
    return db_session.query(Farm).filter(Farm.url == farm_url).first()

def get_multi(db_session, *, skip=0, limit=100) -> List[Optional[Farm]]:
    return db_session.query(Farm).offset(skip).limit(limit).all()

def create(db_session, *, farm_in: FarmInCreate) -> Farm:
    farm = Farm(
        farm_name=farm_in.farm_name,
        url=farm_in.url,
        username=farm_in.username,
        password=farm_in.password,
        is_authenticated=farm_in.is_authenticated
    )
    db_session.add(farm)
    db_session.commit()
    db_session.refresh(farm)
    return farm

def is_authenticated(Farm):
    return farm.is_authenticated
