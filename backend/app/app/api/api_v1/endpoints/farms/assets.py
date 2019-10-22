from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from starlette.requests import Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.api.utils.farms import get_farm_list

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
    farm_id: List[int] = Query(None),
    farm_url: str = Query(None),
    db: Session = Depends(get_db),
):
    farm_list = get_farm_list(db, farm_id_list=farm_id, farm_url=farm_url)

    query_params = {**request.query_params}
    query_params.pop('farm_id', None)
    query_params.pop('farm_url', None)

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
    farm_id: List[int] = Query(None),
    farm_url: str = Query(None),
    #filters: Dict = Query(None),
    db: Session = Depends(get_db),
):
    farm_list = get_farm_list(db, farm_id_list=farm_id, farm_url=farm_url)

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
    farm_id: List[int] = Query(None),
    farm_url: str = Query(None),
    db: Session = Depends(get_db),
):
    farm_list = get_farm_list(db, farm_id_list=farm_id, farm_url=farm_url)

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
    farm_id: List[int] = Query(None),
    farm_url: str = Query(None),
    db: Session = Depends(get_db),
):
    farm_list = get_farm_list(db, farm_id_list=farm_id, farm_url=farm_url)

    data = {}
    for farm in farm_list:
        data[farm.id] = []
        f = farmOS(farm.url, farm.username, farm.password)
        if f.authenticate() :
            data[farm.id].append(f.asset.delete(id=id))

    return data
