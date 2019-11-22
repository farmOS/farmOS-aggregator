from typing import List

from fastapi import APIRouter, Body, Depends, Security, HTTPException, Query
from sqlalchemy.orm import Session
import requests
import time

from app import crud
from app.api.utils.db import get_db
from app.api.utils.farms import get_farm_client, ClientError, get_farms_url_or_list, get_farm_by_id
from app.api.utils.security import get_farm_access
from app.models.farm import Farm, FarmCreate, FarmUpdate
from app.models.farm_token import FarmTokenCreate, FarmAuthorizationParams

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


@router.put(
    "/{farm_id}/authorize/",
    dependencies=[Security(get_farm_access, scopes=['farm:authorize'])]
)
def authorize_farm(
    farm: Farm = Depends(get_farm_by_id),
    *,
    db: Session = Depends(get_db),
    auth_params: FarmAuthorizationParams,
):
    """
    Authorize a farm. Complete the OAuth Authorization Flow.
    """
    data = {}
    data['code'] = auth_params.code
    data['state'] = auth_params.state
    data['grant_type'] = auth_params.grant_type
    data['client_id'] = auth_params.client_id
    data['redirect_uri'] = farm.url + "/api/authorized"

    if auth_params.client_secret is not None:
        data['client_secret'] = auth_params.client_secret

    if auth_params.redirect_uri is not None:
        data['redirect_uri'] = auth_params.redirect_uri

    token_url = farm.url + "/oauth2/token"

    response = requests.post(token_url, data)

    if response.status_code == 200:
        response_token = response.json()
        if "expires_at" not in response_token:
            response_token['expires_at'] = str(time.time() + int(response_token['expires_in']))
        new_token = FarmTokenCreate(farm_id=farm.id, **response_token)

        old_token = crud.farm_token.get_farm_token(db, farm.id)
        if old_token is None:
            token = crud.farm_token.create_farm_token(db, token=new_token)
        else:
            token = crud.farm_token.update_farm_token(db, token=old_token, token_in=new_token)

        return token
    else:
        return response.content


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

