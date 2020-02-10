import os
import logging
from datetime import datetime

from fastapi import APIRouter, Depends, Security, HTTPException, Body
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from farmOS import farmOS
from farmOS.config import ClientConfig

from app import crud
from app.api.utils.db import get_db
from app.core.config import settings
from app.api.utils.security import get_current_active_superuser
from app.core.celery_app import celery_app
from app.schemas.msg import Msg
from app.schemas.user import UserInDB
from app.schemas.farm import Farm
from app.schemas.farm_token import FarmTokenCreate, FarmAuthorizationParams
from app.api.utils.farms import get_farm_by_id, get_oauth_token
from app.api.utils.security import get_farm_access, get_farm_access_allow_public
from app.utils import send_test_email, generate_farm_authorization_link, generate_farm_registration_link

logger = logging.getLogger(__name__)

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


@router.post(
    "/farm-registration-link",
    dependencies=[Security(get_farm_access, scopes=['farm:create'])]
)
def farm_registration_link(
):
    link = generate_farm_registration_link()
    return link


@router.post("/farm-auth-link/{farm_id}")
def farm_auth_link(
    farm: Farm = Depends(get_farm_by_id),
):
    link = generate_farm_authorization_link(farm.id)
    return link


@router.post(
    "/authorize-farm/",
    dependencies=[Security(get_farm_access_allow_public, scopes=['farm:create'])]
)
def authorize_farm(
        *,
        db: Session = Depends(get_db),
        farm_url: str = Body(...),
        auth_params: FarmAuthorizationParams,
):
    """
    Authorize a new farm. Complete the OAuth Authorization Flow.

    This endpoint is only used when authorizing a new farm, before creation.
    See /authorize-farm/{farm_id} for authorizing existing farms.
    """
    logging.debug("Authorizing new farm: " + farm_url)

    token = get_oauth_token(farm_url, auth_params)

    # Check the token expiration time.
    if token is not None and 'expires_at' in token:
        # Create datetime objects for comparison.
        now = datetime.now()
        expiration_time = datetime.fromtimestamp(float(token['expires_at']))

        # Calculate seconds until expiration.
        timedelta = expiration_time - now
        expires_in = timedelta.total_seconds()

        # Update the token expires_in value
        token['expires_in'] = expires_in

    client_id = settings.AGGREGATOR_OAUTH_CLIENT_ID
    client_secret = settings.AGGREGATOR_OAUTH_CLIENT_SECRET

    # Allow OAuth over http
    if settings.AGGREGATOR_OAUTH_INSECURE_TRANSPORT:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    try:
        logging.debug("Testing OAuth token with farmOS client.")
        logging.debug(token.dict())
        client = farmOS(
            hostname=farm_url,
            client_id=client_id,
            client_secret=client_secret,
            scope=auth_params.scope,
            token=token.dict(),
        )
        info = client.info()

        return {
            'token': token,
            'info': info
        }
    except Exception as e:
        logging.debug("Error testing OAuth token with farmOS client: ")
        logging.debug(e)
        raise HTTPException(status_code=400, detail="Could not authenticate with farmOS server.")


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
    Authorize an existing farm. Complete the OAuth Authorization Flow.
    """
    token = get_oauth_token(farm.url, auth_params)

    new_token = FarmTokenCreate(farm_id=farm.id, **token.dict())

    old_token = crud.farm_token.get_farm_token(db, farm.id)
    if old_token is None:
        token = crud.farm_token.create_farm_token(db, token=new_token)
    else:
        token = crud.farm_token.update_farm_token(db, token=old_token, token_in=new_token)

    return token


@router.post(
    "/validate-farm-url",
    dependencies=[Security(get_farm_access_allow_public)]
)
def validate_farm_url(
        *,
        db: Session = Depends(get_db),
        farm_url: str = Body(..., embed=True),
):
    """
    Validate the farm_url when registering a new farm.
    Check to make sure the url is not already in use, and check that
    the url points to a valid farmOS server.
    """
    existing_farm = crud.farm.get_by_url(db, farm_url=farm_url)
    if existing_farm:
        raise HTTPException(
            status_code=409,
            detail="A farm with this URL already exists.",
        )

    # Check that the `farm.json` endpoint returns 200
    # TODO: Use farmOS.py helper function to validate server hostname.
    response = {}
    success = True
    if not success:
        raise HTTPException(
            status_code=406,
            detail="Invalid farmOS hostname. Make sure this is a valid hostname for your farmOS Server.",
        )

    return response

