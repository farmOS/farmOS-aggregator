from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from starlette.requests import Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.db_models.farm import Farm as DBFarm
from app.models.farm import Farm, FarmCreate, FarmInDB

from farmOS import farmOS

router = APIRouter()

# /farms/ endpoints for farmOS instances

@router.get("/", tags=["farms"], response_model=List[Farm])
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

@router.get("/{farm_id}", tags=["farms"], response_model=Farm)
def read_farm_by_id(
    farm_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific farm by id
    """
    farm = crud.farm.get_by_id(db, farm_id=farm_id)
    return farm

@router.get("/{farm_url}", tags=["farms"], response_model=Farm)
def read_farm_by_url(
    farm_url: str,
    db: Session = Depends(get_db),
):
    """
    Get a specific farm by farm_url
    """
    farm = crud.farm.get_by_url(db, farm_url=farm_url)
    return farm

@router.post("/", tags=["farms"], response_model=Farm)
async def create_farm(
    *,
    db: Session = Depends(get_db),
    farm_in: FarmCreate
):
    """
    Create new farm
    """
    # Check to see if farm authenticates
    #farm_test = farmOS(farm_in.url, farm_in.username, farm_in.password)
    #farm_in.is_authenticated = farm_test.authenticate()

    farm = crud.farm.create(db, farm_in=farm_in)

    return farm

@router.delete("/{farm_id}", tags=["farms"], response_model=Farm)
async def delete_farm(
    farm_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete farm
    """
    farm = crud.farm.delete(db, farm_id=farm_id)
    return farm

# /farms/info/ endpoint for accessing farmOS info

@router.get("/info/", tags=["farm info"])
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

@router.get("/logs/", tags=["farm log"])
def get_all_farm_logs(
    request: Request,
    db: Session = Depends(get_db),
    farms: List[int] = Query(None),
):
    if farms:
        farm_list = crud.farm.get_by_multi_id(db, farm_id_list=farms)
    else:
        farm_list = crud.farm.get_multi(db)
    query_params = {**request.query_params}
    query_params.pop('farms')

    data = {}
    for farm in farm_list:
        data[farm.id] = []
        f = farmOS(farm.url, farm.username, farm.password)
        if f.authenticate() :
            data[farm.id] = data[farm.id] + f.log.get(filters=query_params)
    return data

@router.post("/logs/", tags=["farm log"])
def create_farm_logs(
    log: Log,
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
            data[farm.id].append(f.log.send(payload=log.dict()))

    return data


    return data

# /farms/assets/ endpoint for accessing farmOS assets

class Asset(BaseModel):
    class Config:
        extra = 'allow'

    name: str
    type: str

class AssetUpdate(BaseModel):
    class Config:
        extra = 'allow'

    id: int

@router.get("/assets/", tags=["farm asset"])
def get_all_farm_assets(
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
            data[farm.id] = data[farm.id] + f.asset.get()

    return data

@router.post("/assets/", tags=["farm asset"])
def create_farm_assets(
    asset: Asset,
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
            data[farm.id] = data[farm.id] + f.asset.send(payload=asset.dict())


    return data

# /farms/terms/ endpoint for accessing farmOS terms

@router.get("/terms/", tags=["farm term"])
def get_all_farm_terms(
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
            data[farm.id] = data[farm.id] + f.term.get()

    return data

# /farms/areas/ endpoint for accessing farmOS areas

@router.get("/areas/", tags=["farm area"])
def get_all_farm_areas(
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
            data[farm.id] = data[farm.id] + f.area.get()

    return data
