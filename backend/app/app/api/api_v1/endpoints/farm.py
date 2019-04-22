from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.db_models.farm import Farm as DBFarm
from app.models.farm import Farm, FarmInCreate, FarmInDB

from farmOS import farmOS

router = APIRouter()

# /farms/ endpoints for farmOS instances

@router.get("/farms/", tags=["farms"], response_model=List[Farm])
def read_farms(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve farms
    """
    farms = crud.farm.get_multi(db, skip=skip, limit=limit)
    return farms

@router.get("/farms/{farm_id}", tags=["farms"], response_model=Farm)
def read_farm_by_id(
    farm_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific farm by id
    """
    farm = curd.farm.get_by_id(db, farm_id=farm_id)

@router.get("/farms/{farm_url}", tags=["farms"], response_model=Farm)
def read_farm_by_url(
    farm_url: str,
    db: Session = Depends(get_db),
):
    """
    Get a specific farm by farm_url
    """
    farm = curd.farm.get_by_url(db, farm_url=farm_url)

@router.post("/farms/", tags=["farms"], response_model=Farm)
async def create_farm(
    *,
    db: Session = Depends(get_db),
    farm_in: FarmInCreate
):
    """
    Create new farm
    """
    # Check to see if farm authenticates
    farm_test = farmOS(farm_in.url, farm_in.username, farm_in.password)
    farm_in.is_authenticated = farm_test.authenticate()

    farm = crud.farm.create(db, farm_in=farm_in)

    return farm

# /farms/info/ endpoint for accessing farmOS info

@router.get("/farms/info/", tags=["farm info"])
def get_all_farm_info(
    farms: List[int] = Query(None),
    db: Session = Depends(get_db),
):
    if farms:
        farm_list = crud.farm.get_by_multi_id(db, farm_id_list=farms)
    else:
        farm_list = crud.farm.get_multi(db)

    data = {}
    for farm in farm_list:
        data[farm.id] = {}
        f = farmOS(farm.url, farm.username, farm.password)
        if f.authenticate() :
            data[farm.id]['info'] = f.info()

    return data

# /farms/logs/ endpoint for accessing farmOS logs

class Log(BaseModel):
    class Config:
        extra = 'allow'

    name: str
    type: str

class LogUpdate(BaseModel):
    class Config:
        extra = 'allow'

    id: int

@router.get("/farms/logs/", tags=["farm log"])
def get_all_farm_logs(
    farms: List[int] = Query(None),
    #filters: Dict = Query(None),
    db: Session = Depends(get_db),
):
    if farms:
        farm_list = crud.farm.get_by_multi_id(db, farm_id_list=farms)
    else:
        farm_list = crud.farm.get_multi(db)

    data = {}
    for farm in farm_list:
        data[farm.id] = []
        f = farmOS(farm.url, farm.username, farm.password)
        if f.authenticate() :
            data[farm.id].append(f.log.get())

    return data

