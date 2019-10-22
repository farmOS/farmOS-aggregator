from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from starlette.requests import Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.api.utils.farms import get_farm_list

from farmOS import farmOS

router = APIRouter()

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

@router.get("/")
def get_all_farm_logs(
    request: Request,
    farm_url: str = Query(None),
    farm_id: List[int] = Query(None),
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
            data[farm.id] = data[farm.id] + f.log.get(filters=query_params)
    return data

@router.post("/")
def create_farm_logs(
    log: Log,
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
            data[farm.id].append(f.log.send(payload=log.dict()))

    return data

@router.put("/")
def update_farm_logs(
    log: LogUpdate,
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
            data[farm.id].append(f.log.send(payload=log.dict()))

    return data

@router.delete("/")
def delete_farm_logs(
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
            data[farm.id].append(f.log.delete(id=id))

    return data
