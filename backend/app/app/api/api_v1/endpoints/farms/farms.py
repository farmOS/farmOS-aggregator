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

# /farms/ endpoints for farmOS instances

@router.get("/", response_model=List[Farm])
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

@router.get("/{farm_id}", response_model=Farm)
def read_farm_by_id(
    farm_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific farm by id
    """
    farm = crud.farm.get_by_id(db, farm_id=farm_id)
    return farm

@router.post("/", response_model=Farm)
async def create_farm(
    *,
    db: Session = Depends(get_db),
    farm_in: FarmCreate
):
    """
    Create new farm
    """
    existing_farm = crud.farm.get_by_url(db, farm_url=farm_in.url)
    if existing_farm:
        raise HTTPException(
            status_code=409,
            detail="A farm with this URL already exists.",
        )

    farm = crud.farm.create(db, farm_in=farm_in)

    return farm

@router.put("/{farm_id}", response_model=Farm)
async def update_farm(
    *,
    db: Session = Depends(get_db),
    farm_id: int,
    farm_in: FarmUpdate,
):
    """
    Update farm
    """
    farm = crud.farm.get_by_id(db, farm_id=farm_id)
    if not farm:
        raise HTTPException(
            status_code=404,
            detail="The farm with this ID does not exist in the system",
        )
    farm = crud.farm.update(db, farm=farm, farm_in=farm_in)
    return farm

@router.delete("/{farm_id}", response_model=Farm)
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
