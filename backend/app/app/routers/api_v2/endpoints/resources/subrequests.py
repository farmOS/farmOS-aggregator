from fastapi import APIRouter, Depends
from pydantic.typing import List
from sqlalchemy.orm import Session
from farmOS.subrequests import Subrequest, Format

from app.routers.utils.db import get_db
from app.routers.utils.farms import get_active_farms_url_or_list, get_farm_client, ClientError
from app.schemas.farm import Farm

router = APIRouter()

# /farms/resources/subrequests endpoint.


@router.post("")
def send_subrequests(
    blueprint: List[Subrequest],
    farm_list: List[Farm] = Depends(get_active_farms_url_or_list),
    db: Session = Depends(get_db),
):
    data = {}
    for farm in farm_list:
        data[farm.id] = []

        # Get a farmOS client.
        try:
            farm_client = get_farm_client(db=db, farm=farm)
        except ClientError as e:
            data[farm.id] = str(e)
            continue

        # Make the request.
        try:
            data[farm.id] = farm_client.subrequests.send(blueprint, Format.json)
        except Exception as e:
            data[farm.id] = str(e)
            continue

    return data
