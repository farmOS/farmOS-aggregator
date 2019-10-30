from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from starlette.requests import Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.api.utils.farms import get_farm_list, get_farm_client, ClientError

from farmOS import farmOS

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

        # Get a farmOS client.
        try:
            farm_client = get_farm_client(db_session=db, farm=farm)
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
    farm_id: List[int] = Query(None),
    farm_url: str = Query(None),
    db: Session = Depends(get_db),
):
    farm_list = get_farm_list(db, farm_id_list=farm_id, farm_url=farm_url)

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
            data[farm.id].append(farm_client.term.send(payload=term.dict()))
        except:
            continue

    return data

@router.put("/")
def update_farm_terms(
    term: TermUpdate,
    farm_id: List[int] = Query(None),
    farm_url: str = Query(None),
    db: Session = Depends(get_db),
):
    farm_list = get_farm_list(db, farm_id_list=farm_id, farm_url=farm_url)

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
            data[farm.id].append(farm_client.term.send(payload=term.dict()))
        except:
            continue

    return data

@router.delete("/")
def delete_farm_term(
    tid: int,
    farm_id: List[int] = Query(None),
    farm_url: str = Query(None),
    db: Session = Depends(get_db),
):
    farm_list = get_farm_list(db, farm_id_list=farm_id, farm_url=farm_url)

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
            data[farm.id].append(farm_client.term.delete(id=tid))
        except:
            continue

    return data
