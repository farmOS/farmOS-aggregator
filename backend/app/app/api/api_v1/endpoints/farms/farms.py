from typing import List

from fastapi import APIRouter, Body, Depends, Security, HTTPException, Query
from sqlalchemy.orm import Session


from app import crud
from app.api.utils.db import get_db
from app.api.utils.farms import get_farm_client, ClientError, get_farms_url_or_list, get_farm_by_id
from app.api.utils.security import get_farm_access
from app.models.farm import Farm, FarmCreate, FarmUpdate

router = APIRouter()

# /farms/ endpoints for farmOS instances

@router.get(
    "/",
    response_model=List[Farm],
    dependencies=[Security(get_farm_access, scopes=['farm:read'])]
)
def read_farms(
    farms: List[Farm] = Depends(get_farms_url_or_list),
):
    """
    Retrieve farms
    """
    return farms


@router.get(
    "/{farm_id}",
    response_model=Farm,
    dependencies=[Security(get_farm_access, scopes=['farm:read'])]
)
def read_farm_by_id(
    farm: Farm = Depends(get_farm_by_id)
):
    """
    Get a specific farm by id
    """
    return farm


@router.post(
    "/",
    response_model=Farm,
    dependencies=[Security(get_farm_access, scopes=['farm:create'])]
)
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


@router.put(
    "/{farm_id}",
    response_model=Farm,
    dependencies=[Security(get_farm_access, scopes=['farm:update'])]
)
async def update_farm(
    *,
    db: Session = Depends(get_db),
    farm: Farm = Depends(get_farm_by_id),
    farm_in: FarmUpdate,
):
    """
    Update farm
    """
    if farm_in.url is not None:
        existing_farm = crud.farm.get_by_url(db, farm_url=farm_in.url)
        if existing_farm:
            raise HTTPException(
                status_code=409,
                detail="A farm with this URL already exists.",
            )

    farm = crud.farm.update(db, farm=farm, farm_in=farm_in)
    return farm


@router.delete(
    "/{farm_id}",
    response_model=Farm,
    dependencies=[Security(get_farm_access, scopes=['farm:delete'])]
)
async def delete_farm(
    farm_id: int,
    db: Session = Depends(get_db),
    farm: Farm = Depends(get_farm_by_id)
):
    """
    Delete farm
    """
    farm = crud.farm.delete(db, farm_id=farm_id)
    return farm

# /farms/info/ endpoint for accessing farmOS info


@router.get(
    "/info/",
    dependencies=[Security(get_farm_access, scopes=['farm.info'])],
    tags=["farm info"]
)
def get_all_farm_info(
    db: Session = Depends(get_db),
    farm_list: List[Farm] = Depends(get_farms_url_or_list)
):
    data = {}
    for farm in farm_list:
        data[farm.id] = {}
        try:
            farm_client = get_farm_client(db_session=db, farm=farm)
        except ClientError:
            continue

        try:
            data[farm.id]['info'] = farm_client.info()
        except:
            continue

    return data

