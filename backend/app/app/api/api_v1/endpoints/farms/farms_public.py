import logging
from typing import List
import time

from fastapi import APIRouter, Body, Depends, Security, HTTPException, Body
from sqlalchemy.orm import Session
import requests
from farmOS import farmOS
from farmOS.config import ClientConfig
from app.core.celery_app import celery_app


from app.core import config
from app import crud
from app.api.utils.db import get_db
from app.api.utils.farms import get_oauth_token
from app.models.farm import Farm, FarmCreate
from app.models.farm_token import FarmAuthorizationParams

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/",
    response_model=Farm,
)
async def create_farm(
    *,
    db: Session = Depends(get_db),
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

    farm = crud.farm.create(db, farm_in=farm_in)

    celery_app.send_task("app.worker.ping_farm", [farm.id])

    return farm


@router.post(
    "/authorize-farm/",
)
def authorize_farm(
        *,
        db: Session = Depends(get_db),
        farm_url: str = Body(...),
        auth_params: FarmAuthorizationParams,
):
    """
    Authorize a farm. Complete the OAuth Authorization Flow.
    """
    token = get_oauth_token(farm_url, auth_params)

    client_id = 'farmos_api_client'
    client_secret = 'client_secret'

    config = ClientConfig()

    config_values = {
        'Profile': {
            'development': 'True',
            'hostname': farm_url,
            'client_id': client_id,
            'client_secret': client_secret,
        }
    }

    if token is not None:
        config_values['Profile']['access_token'] = token.access_token
        config_values['Profile']['refresh_token'] = token.refresh_token
        config_values['Profile']['expires_at'] = token.expires_at
    config.read_dict(config_values)

    try:
        client = farmOS(config=config, profile_name="Profile")
        info = client.info()

        return {
            'token': token,
            'info': info
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Could not authenticate with farmOS server.")

