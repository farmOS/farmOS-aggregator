import logging
import os
from datetime import datetime

from farmOS import farmOS
from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Security
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud
from app.core.jwt import create_farm_api_token
from app.routers.utils.db import get_db
from app.routers.utils.farms import (
    build_farm_url,
    get_farm_by_id,
    get_farm_client,
    get_oauth_token,
    handle_ping_farms,
)
from app.routers.utils.security import get_farm_access, get_farm_access_allow_public
from app.schemas.farm import Farm
from app.schemas.farm_token import FarmAuthorizationParams, FarmTokenCreate
from app.schemas.msg import Msg
from app.utils import (
    generate_farm_authorization_link,
    generate_farm_registration_link,
    get_settings,
    send_farm_authorization_email,
    send_farm_registration_email,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/ping-farms/",
    dependencies=[Security(get_farm_access)],
    response_model=Msg,
    status_code=200,
)
def ping_farms(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    settings=Depends(get_settings),
):
    """
    Ping all active farms.
    """
    background_tasks.add_task(handle_ping_farms, db, settings)
    return {"msg": f"Created background task to ping farms."}


@router.post(
    "/farm-registration-link",
    dependencies=[Security(get_farm_access, scopes=["farm:create"])],
)
def farm_registration_link():
    link = generate_farm_registration_link()
    return link


@router.post(
    "/send-farm-registration-email/",
    dependencies=[Security(get_farm_access, scopes=["farm:create"])],
    response_model=Msg,
    status_code=201,
)
def send_registration_email(
    email_to: EmailStr,
):
    """
    Test emails.
    """
    link = generate_farm_registration_link()
    send_farm_registration_email(email_to=email_to, link=link)
    return {"msg": "Registration email sent to: " + email_to}


@router.post("/farm-auth-link/{farm_id}")
def farm_auth_link(
    farm: Farm = Depends(get_farm_by_id),
):
    link = generate_farm_authorization_link(farm.id)
    return link


@router.post(
    "/send-farm-authorization-email/",
    dependencies=[Security(get_farm_access, scopes=["farm:create"])],
    response_model=Msg,
    status_code=201,
)
def send_registration_email(email_to: EmailStr, farm: Farm = Depends(get_farm_by_id)):
    """
    Test emails.
    """
    link = generate_farm_authorization_link(farm.id)
    send_farm_authorization_email(email_to=email_to, link=link, farm=farm)
    return {"msg": "Authorization email sent to: " + email_to}


@router.post(
    "/authorize-farm/",
    dependencies=[Security(get_farm_access_allow_public, scopes=["farm:create"])],
)
def authorize_farm(
    *,
    db: Session = Depends(get_db),
    farm_url: str = Body(...),
    auth_params: FarmAuthorizationParams,
    settings=Depends(get_settings),
):
    """
    Authorize a new farm. Complete the OAuth Authorization Flow.

    This endpoint is only used when authorizing a new farm, before creation.
    See /authorize-farm/{farm_id} for authorizing existing farms.
    """
    logging.debug("Authorizing new farm: " + farm_url)

    try:
        token = get_oauth_token(farm_url, auth_params)
    except Exception as e:
        error = f"Authorization flow failed: {e}"
        raise HTTPException(
            status_code=400,
            detail=error,
        )

    # Check the token expiration time.
    if token is not None and "expires_at" in token:
        # Create datetime objects for comparison.
        now = datetime.now()
        expiration_time = datetime.fromtimestamp(float(token["expires_at"]))

        # Calculate seconds until expiration.
        timedelta = expiration_time - now
        expires_in = timedelta.total_seconds()

        # Update the token expires_in value
        token["expires_in"] = expires_in

    client_id = settings.AGGREGATOR_OAUTH_CLIENT_ID
    client_secret = settings.AGGREGATOR_OAUTH_CLIENT_SECRET

    # Allow OAuth over http
    if settings.AGGREGATOR_OAUTH_INSECURE_TRANSPORT:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    try:
        logging.debug("Testing OAuth token with farmOS client.")
        logging.debug(token.dict())
        version = 2 if len(token.access_token) > 60 else 1
        client = farmOS(
            hostname=farm_url,
            client_id=client_id,
            client_secret=client_secret,
            scope=auth_params.scope,
            token=token.dict(),
            version=version,
        )

        # Set the info depending on v1 or v2.
        # v2 provides info under the meta.farm key.
        response = client.info()
        if "meta" in response:
            info = response["meta"]["farm"]
        else:
            info = response

        return {"token": token, "info": info}
    except Exception as e:
        logging.debug("Error testing OAuth token with farmOS client: ")
        logging.debug(e)
        raise HTTPException(
            status_code=400, detail="Could not authenticate with farmOS server."
        )


@router.post(
    "/authorize-farm/{farm_id}",
    dependencies=[Security(get_farm_access_allow_public, scopes=["farm:authorize"])],
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
    try:
        token = get_oauth_token(farm.url, auth_params)
    except Exception as e:
        error = f"Authorization flow failed: {e}"
        crud.farm.update_is_authorized(
            db, farm_id=farm.id, is_authorized=False, auth_error=error
        )
        raise HTTPException(
            status_code=400,
            detail=error,
        )

    new_token = FarmTokenCreate(farm_id=farm.id, **token.dict())

    old_token = crud.farm_token.get_farm_token(db, farm.id)
    if old_token is None:
        token = crud.farm_token.create_farm_token(db, token=new_token)
    else:
        token = crud.farm_token.update_farm_token(
            db, token=old_token, token_in=new_token
        )

    # Update the scope attribute of the Farm profile to the scope that was just authorized.
    crud.farm.update_scope(db, farm=farm, scope=auth_params.scope)

    # Reconnect to the farmOS server and update farm info.
    try:
        version = 2 if len(new_token.access_token) > 60 else 1
        farm_client = get_farm_client(db=db, farm=farm, version=version)

        response = farm_client.info()
        # Set the info depending on v1 or v2.
        # v2 provides info under the meta.farm key.
        if "meta" in response:
            info = response["meta"]["farm"]
        else:
            info = response

        crud.farm.update_info(db, farm=farm, info=info)
    except Exception as e:
        error = f"Could not connect to farm after successful Authorization Flow: {e}"
        crud.farm.update_is_authorized(
            db, farm_id=farm.id, is_authorized=False, auth_error=error
        )
        raise HTTPException(
            status_code=400,
            detail=error,
        )

    return {"token": token, "info": info}


@router.post(
    "/validate-farm-url", dependencies=[Security(get_farm_access_allow_public)]
)
def validate_farm_url(
    *,
    db: Session = Depends(get_db),
    farm_url: str = Body(..., embed=True),
    settings=Depends(get_settings),
):
    """
    Validate the farm_url when registering a new farm.
    Check to make sure the url is not already in use, and check that
    the url points to a valid farmOS server.
    """
    try:
        clean_url = build_farm_url(farm_url)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid url: {e}",
        )
    # Check that the `farm.json` endpoint returns 200
    # TODO: Use farmOS.py helper function to validate server hostname.
    success = True
    if not success:
        raise HTTPException(
            status_code=406,
            detail="Invalid farmOS hostname. Make sure this is a valid hostname for your farmOS Server.",
        )

    farm_id = None
    api_token = None
    existing_farm = crud.farm.get_by_url(db, farm_url=clean_url)
    if existing_farm is not None:
        farm_id = existing_farm.id
        api_token = create_farm_api_token(farm_id=[farm_id], scopes=["farm:authorize"])
    elif settings.AGGREGATOR_OPEN_FARM_REGISTRATION is True:
        api_token = create_farm_api_token(farm_id=[], scopes=["farm:create"])

    return {"id": farm_id, "api_token": api_token}
