from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from starlette.requests import Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.db_models.farm import Farm as DBFarm
from app.models.farm import Farm, FarmCreate, FarmUpdate, FarmInDB

from farmOS import farmOS

router = APIRouter()

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

@router.get("/")
def get_all_farm_assets(
    request: Request,
    farms: List[int] = Query(None),
    db: Session = Depends(get_db),
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
            data[farm.id] = data[farm.id] + f.asset.get(filters=query_params)

    return data

@router.post("/")
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
            data[farm.id].append(f.asset.send(payload=asset.dict()))


    return data

@router.put("/")
def update_farm_assets(
    asset: AssetUpdate,
    farms: List[int] = Query(None),
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
            data[farm.id].append(f.asset.send(payload=asset.dict()))

    return data

@router.delete("/")
def delete_farm_assets(
    id: int,
    farms: List[int] = Query(None),
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
            data[farm.id].append(f.asset.delete(id=id))

    return data
