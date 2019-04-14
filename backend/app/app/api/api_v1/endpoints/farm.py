from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
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

# /farms/logs/ endpoint for accessing farmOS logs

# @router.get("/farm/logs/", tags=["farm"])
# def get_all_farm_logs():
#     data = []
#     for farm in farms:
#         response = await farm.log.get()
#         data.append(response)
#
#     return data
