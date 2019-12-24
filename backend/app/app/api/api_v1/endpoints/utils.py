from fastapi import APIRouter, Depends, Security, HTTPException
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
from app.api.utils.farms import get_farm_by_id, get_oauth_token
from app.api.utils.security import get_farm_access
from app.utils import send_test_email, generate_farm_authorization_link

router = APIRouter()


@router.post("/ping-farms/", response_model=Msg, status_code=201)
def ping_farms(
    current_user: UserInDB = Depends(get_current_active_superuser)
):
    """
    Ping all farms.
    """
    celery_app.send_task("app.worker.ping_farms")
    return {"msg": "Task created. Check farm last_updated values."}


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
    token = get_oauth_token(farm.url, auth_params)

    new_token = FarmTokenCreate(farm_id=farm.id, **token.dict())

    old_token = crud.farm_token.get_farm_token(db, farm.id)
    if old_token is None:
        token = crud.farm_token.create_farm_token(db, token=new_token)
    else:
        token = crud.farm_token.update_farm_token(db, token=old_token, token_in=new_token)

    return token
