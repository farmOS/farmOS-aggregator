from typing import List

from fastapi import APIRouter, Body, Depends, Security, HTTPException, Query
from pydantic.typing import Optional
from sqlalchemy.orm import Session


from app import crud
from app.utils import get_settings
from app.routers.utils.db import get_db
from app.routers.utils.farms import (
    ClientError,
    get_farm_client,
    get_farms_url_or_list,
    get_farm_by_id,
    admin_alert_email,
)
from app.routers.utils.security import get_farm_access, get_farm_access_allow_public
from app.schemas.farm import Farm, AllFarmInfo, FarmCreate, FarmUpdate

router = APIRouter()

# /farms/ endpoints for farmOS instances


@router.get(
    "/",
    response_model=List[Farm],
    dependencies=[Security(get_farm_access, scopes=["farm:read"])],
)
def read_farms(
    farms: List[Farm] = Depends(get_farms_url_or_list),
):
    """
    Retrieve farms
    """
    return farms


# /farms/info/ endpoint for accessing farmOS info
@router.get(
    "/info",
    dependencies=[Security(get_farm_access, scopes=["farm:read", "farm.info"])],
    tags=["farm info"],
)
def get_all_farm_info(
    db: Session = Depends(get_db),
    farm_list: List[Farm] = Depends(get_farms_url_or_list),
    use_cached: Optional[bool] = True,
):
    data = {}
    for farm in farm_list:
        data[farm.id] = {}

        if use_cached:
            data[farm.id] = farm.info
        else:

            # Determine the correct version
            version = 2 if len(farm.token.access_token) > 60 else 1
            try:
                farm_client = get_farm_client(db=db, farm=farm, version=version)
            except ClientError as e:
                data[farm.id] = str(e)

            try:
                response = farm_client.info()
                # Set the info depending on v1 or v2.
                # v2 provides info under the meta.farm key.
                if "meta" in response:
                    info = response["meta"]["farm"]
                else:
                    info = response
                data[farm.id]["info"] = info

                crud.farm.update_info(db, farm=farm, info=info)
            except:
                continue

    return data


@router.get(
    "/{farm_id}",
    response_model=AllFarmInfo,
    dependencies=[Security(get_farm_access, scopes=["farm:read"])],
)
def read_farm_by_id(farm: Farm = Depends(get_farm_by_id)):
    """
    Get a specific farm by id
    """
    return farm


@router.post(
    "/",
    response_model=Farm,
    dependencies=[Security(get_farm_access_allow_public, scopes=["farm:create"])],
)
async def create_farm(
    *,
    db: Session = Depends(get_db),
    settings=Depends(get_settings),
    farm_in: FarmCreate,
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

    if settings.AGGREGATOR_ALERT_NEW_FARMS:
        admin_alert_email(
            db=db,
            message="New farm created: " + farm_in.farm_name + " - " + farm_in.url,
        )

    farm = crud.farm.create(db, farm_in=farm_in)

    return farm


@router.put(
    "/{farm_id}",
    response_model=Farm,
    dependencies=[Security(get_farm_access, scopes=["farm:update"])],
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
    dependencies=[Security(get_farm_access, scopes=["farm:delete"])],
)
async def delete_farm(
    farm_id: int, db: Session = Depends(get_db), farm: Farm = Depends(get_farm_by_id)
):
    """
    Delete farm
    """
    farm = crud.farm.delete(db, farm_id=farm_id)
    return farm
