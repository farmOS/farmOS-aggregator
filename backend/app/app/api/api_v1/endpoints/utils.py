import time

import requests
from fastapi import APIRouter, Depends, Security
from pydantic.types import EmailStr
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_superuser
from app.core.celery_app import celery_app
from app.models.msg import Msg
from app.models.user import UserInDB
from app.models.farm import Farm
from app.models.farm_token import FarmTokenCreate, FarmAuthorizationParams
from app.api.utils.farms import get_farm_by_id
from app.api.utils.security import get_farm_access
from app.utils import send_test_email, generate_farm_authorization_link

router = APIRouter()


@router.post("/test-celery/", response_model=Msg, status_code=201)
def test_celery(
    msg: Msg, current_user: UserInDB = Depends(get_current_active_superuser)
):
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=Msg, status_code=201)
def test_email(
    email_to: EmailStr, current_user: UserInDB = Depends(get_current_active_superuser)
):
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}

@router.post("/farm-auth-link/{farm_id}")
def farm_auth_link(
    farm: Farm = Depends(get_farm_by_id),
):
    link = generate_farm_authorization_link(farm.id)
    return link


@router.post(
    "/authorize-farm/{farm_id}",
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
