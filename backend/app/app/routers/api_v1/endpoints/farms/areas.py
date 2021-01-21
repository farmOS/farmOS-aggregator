from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from starlette.requests import Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.routers.utils.db import get_db
from app.routers.utils.farms import get_active_farms_url_or_list, get_farm_client, ClientError
from app.schemas.farm import Farm

router = APIRouter()

# /farms/areas/ endpoint for accessing farmOS areas


class Area(BaseModel):
    class Config:
        extra = 'allow'

    name: str
    vocabulary: int
    area_type: str


class AreaUpdate(BaseModel):
    class Config:
        extra = 'allow'

    id: int


@router.get("/")
def get_all_farm_areas(
    request: Request,
    farm_list: List[Farm] = Depends(get_active_farms_url_or_list),
    db: Session = Depends(get_db),
):
    query_params = {**request.query_params}
    query_params.pop('farm_id', None)
    query_params.pop('farm_url', None)

    data = {}
    for farm in farm_list:
        data[farm.id] = []

        # Get a farmOS client.
        try:
            farm_client = get_farm_client(db=db, farm=farm, version=1)
        except ClientError:
            continue

        # Make the request.
        try:
            data[farm.id] = data[farm.id] + farm_client.area.get(filters=query_params)['list']
        except:
            continue

    return data


@router.post("/")
def create_farm_area(
    area: Area,
    farm_list: List[Farm] = Depends(get_active_farms_url_or_list),
    db: Session = Depends(get_db),
):
    data = {}
    for farm in farm_list:
        data[farm.id] = []

        # Get a farmOS client.
        try:
            farm_client = get_farm_client(db=db, farm=farm, version=1)
        except ClientError:
            continue


        # Make the request.
        try:
            data[farm.id].append(farm_client.area.send(payload=area.dict()))
        except:
            continue

    return data


@router.put("/")
def update_farm_area(
    area: AreaUpdate,
    farm_list: List[Farm] = Depends(get_active_farms_url_or_list),
    db: Session = Depends(get_db),
):
    data = {}
    for farm in farm_list:
        data[farm.id] = []

        # Get a farmOS client.
        try:
            farm_client = get_farm_client(db=db, farm=farm, version=1)
        except ClientError:
            continue


        # Make the request.
        try:
            data[farm.id].append(farm_client.area.send(payload=area.dict()))
        except:
            continue

    return data


@router.delete("/")
def delete_farm_area(
    id: List[int] = Query(None),
    farm_list: List[Farm] = Depends(get_active_farms_url_or_list),
    db: Session = Depends(get_db),
):
    data = {}
    for farm in farm_list:
        data[farm.id] = []

        # Get a farmOS client.
        try:
            farm_client = get_farm_client(db=db, farm=farm, version=1)
        except ClientError:
            continue

        # Make the request.
        for single_id in id:
            try:
                result = farm_client.area.delete(id=single_id)
                data[farm.id].append({single_id: result.json()})
            except:
                data[farm.id].append({single_id: "error"})
                continue

    return data
