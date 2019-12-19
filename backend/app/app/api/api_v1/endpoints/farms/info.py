from typing import List

from fastapi import APIRouter, Body, Depends, Security, HTTPException, Query
from sqlalchemy.orm import Session


from app import crud
from app.api.utils.db import get_db
from app.api.utils.farms import get_farm_client, ClientError, get_farms_url_or_list
from app.api.utils.security import get_farm_access
from app.models.farm import Farm
from app.models.farm_info import FarmInfo

router = APIRouter()

# /farms/info/ endpoint for accessing farmOS info
@router.get(
    "/",
    dependencies=[Security(get_farm_access, scopes=['farm:read', 'farm.info'])],
    tags=["farm info"]
)
def get_all_farm_info(
        db: Session = Depends(get_db),
        farm_list: List[Farm] = Depends(get_farms_url_or_list),
        use_cached: bool = True,
):
    data = {}
    for farm in farm_list:
        data[farm.id] = {}

        if use_cached:
            data[farm.id] = farm.info
        else:
            try:
                farm_client = get_farm_client(db_session=db, farm=farm)
            except ClientError:
                continue

            try:
                info = farm_client.info()
                data[farm.id]['info'] = info

                crud.farm.update_info(db, farm=farm, info=info)
            except:
                continue

    return data
