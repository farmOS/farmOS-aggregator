from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from starlette.requests import Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.routers.utils.db import get_db
from app.routers.utils.farms import get_active_farms_url_or_list, get_farm_client, ClientError
from app.schemas.farm import Farm

router = APIRouter()

# /farms/terms/ endpoint for accessing farmOS terms


class Term(BaseModel):
    class Config:
        extra = 'allow'

    name: str
    vocabulary: int


class TermUpdate(BaseModel):
    class Config:
        extra = 'allow'

    id: int


@router.get("/")
def get_all_farm_terms(
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
            farm_client = get_farm_client(db=db, farm=farm)
        except ClientError:
            continue

        # Make the request.
        try:
            data[farm.id] = data[farm.id] + farm_client.term.get(filters=query_params)['list']
        except:
            continue

    return data


@router.post("/")
def create_farm_term(
    term: Term,
    farm_list: List[Farm] = Depends(get_active_farms_url_or_list),
    db: Session = Depends(get_db),
):
    data = {}
    for farm in farm_list:
        data[farm.id] = []

        # Get a farmOS client.
        try:
            farm_client = get_farm_client(db=db, farm=farm)
        except ClientError:
            continue

        # Make the request.
        try:
            data[farm.id].append(farm_client.term.send(payload=term.dict()))
        except:
            continue

    return data


@router.put("/")
def update_farm_terms(
    term: TermUpdate,
    farm_list: List[Farm] = Depends(get_active_farms_url_or_list),
    db: Session = Depends(get_db),
):
    data = {}
    for farm in farm_list:
        data[farm.id] = []

        # Get a farmOS client.
        try:
            farm_client = get_farm_client(db=db, farm=farm)
        except ClientError:
            continue

        # Make the request.
        try:
            data[farm.id].append(farm_client.term.send(payload=term.dict()))
        except:
            continue

    return data


@router.delete("/")
def delete_farm_term(
    tid: List[int] = Query(None),
    farm_list: List[Farm] = Depends(get_active_farms_url_or_list),
    db: Session = Depends(get_db),
):
    data = {}
    for farm in farm_list:
        data[farm.id] = []

        # Get a farmOS client.
        try:
            farm_client = get_farm_client(db=db, farm=farm)
        except ClientError:
            continue

        # Make the request.
        for id in tid:
            try:
                result = farm_client.term.delete(id=id)
                data[farm.id].append({id: result.json()})
            except:
                data[farm.id].append({id: "error"})
                continue

    return data
