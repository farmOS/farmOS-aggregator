from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from starlette.requests import Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.api.utils.farms import get_farms_url_or_list, get_farm_client, ClientError
from app.models.farm import Farm

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
    farm_list: List[Farm] = Depends(get_farms_url_or_list),
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
            farm_client = get_farm_client(db_session=db, farm=farm)
        except ClientError:
            continue

        # Make the request.
        try:
            data[farm.id] = data[farm.id] + farm_client.asset.get(filters=query_params)['list']
        except:
            continue

    return data


@router.post("/")
def create_farm_assets(
    asset: Asset,
    farm_list: List[Farm] = Depends(get_farms_url_or_list),
    db: Session = Depends(get_db),
):
    data = {}
    for farm in farm_list:
        data[farm.id] = []

        # Get a farmOS client.
        try:
            farm_client = get_farm_client(db_session=db, farm=farm)
        except ClientError:
            continue

        # Make the request.
        try:
            data[farm.id].append(farm_client.asset.send(payload=asset.dict()))
        except:
            continue

    return data


@router.put("/")
def update_farm_assets(
    asset: AssetUpdate,
    farm_list: List[Farm] = Depends(get_farms_url_or_list),
    db: Session = Depends(get_db),
):
    data = {}
    for farm in farm_list:
        data[farm.id] = []

        # Get a farmOS client.
        try:
            farm_client = get_farm_client(db_session=db, farm=farm)
        except ClientError:
            continue

        # Make the request.
        try:
            data[farm.id].append(farm_client.asset.send(payload=asset.dict()))
        except:
            continue

    return data


@router.delete("/")
def delete_farm_assets(
    id: int,
    farm_list: List[Farm] = Depends(get_farms_url_or_list),
    db: Session = Depends(get_db),
):
    data = {}
    for farm in farm_list:
        data[farm.id] = []

        # Get a farmOS client.
        try:
            farm_client = get_farm_client(db_session=db, farm=farm)
        except ClientError:
            continue

        # Make the request.
        try:
            data[farm.id].append(farm_client.asset.delete(id=id))
        except:
            continue

    return data
