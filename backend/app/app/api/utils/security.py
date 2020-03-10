import logging
import jwt
from fastapi import Depends, HTTPException, Security, Query
from fastapi.security import OAuth2PasswordBearer, APIKeyQuery, APIKeyHeader, SecurityScopes
from jwt import PyJWTError
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED
from pydantic import BaseModel, ValidationError

from app import crud
from app.api.utils.db import get_db
from app.core.config import settings
from app.core.jwt import ALGORITHM
from app.models.user import User
from app.schemas.token import TokenData, FarmAccess


logger = logging.getLogger(__name__)

oauth_scopes = {
    "farm:create": "Create farm profiles",
    "farm:read": "Read farm profiles",
    "farm:update": "Update farm profiles",
    "farm:delete": "Delete farm profiles",
    "farm:authorize": "Complete the OAuth Authorization Code cycle for farm profiles",
    "farm.info": "Read farmOS server info",
    "farm.logs": "Access logs",
    "farm.assets": "Access assets",
    "farm.terms": "Access terms",
    "farm.areas": "Access areas",
}

optional_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token",
    scopes=oauth_scopes,
    auto_error=False
)
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token",
    scopes=oauth_scopes,
    auto_error=True
)

# Define a header to check for API Tokens.
# API Tokens are short-lived JWT Tokens used to authenticate
# farmOS server owners for registration and authorization purposes.
API_TOKEN_NAME = "api-token"
api_token_header = APIKeyHeader(name=API_TOKEN_NAME, auto_error=False)


def get_current_user(
    security_scopes: SecurityScopes,
    db: Session = Depends(get_db),
    token: str = Security(reusable_oauth2)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        token_data = _validate_token(token)
    except (PyJWTError, ValidationError) as e:
        raise credentials_exception

    user = crud.user.get(db, user_id=token_data.user_id)
    if not user:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions."
            )

    return user


def get_current_active_user(current_user: User = Security(get_current_user)):
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(current_user: User = Security(get_current_user)):
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_user_farm_access(
    security_scopes: SecurityScopes,
    db: Session = Depends(get_db),
    token: str = Security(optional_oauth2)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    if token is None:
        # Make this an optional dependency. Don't raise an error if no user is logged in.
        return None
    else:
        try:
            token_data = _validate_token(token)
        except (PyJWTError, ValidationError) as e:
            raise credentials_exception

        user = crud.user.get(db, user_id=token_data.user_id)
        if user is None:
            raise credentials_exception

        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions."
                )

        all_farms = False
        if crud.user.is_superuser(user):
            all_farms = True

        return FarmAccess(scopes=token_data.scopes, user_id=token_data.user_id, all_farms=all_farms)


def get_api_token_farm_access(
    security_scopes: SecurityScopes,
    api_token: str = Security(api_token_header),
):
    if api_token is None:
        return None
    else:
        try:
            token_data = _validate_token(api_token)
        except (PyJWTError, ValidationError) as e:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions."
                )

        return FarmAccess(scopes=token_data.scopes, farm_id_list=token_data.farm_id, all_farms=False)


def get_farm_access(
    user_access: dict = Depends(get_current_user_farm_access),
    api_token_access: dict = Depends(get_api_token_farm_access)
):
    farm_access = None

    if user_access is not None:
        logger.debug(f"Request has user_access: {user_access}")
        farm_access = user_access

    if api_token_access is not None:
        logger.debug(f"Request has api_token access: {api_token_access}")
        farm_access = api_token_access

    if farm_access is None:
        logger.debug(f"Request has no farm access.")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    return farm_access


def get_farm_access_allow_public(
    user_access: dict = Depends(get_current_user_farm_access),
    api_token_access: dict = Depends(get_api_token_farm_access),
):
    farm_access = None

    # If open registration is enabled, allow minimal access.
    if settings.AGGREGATOR_OPEN_FARM_REGISTRATION is True:
        farm_access = FarmAccess(scopes=[], farm_id_list=[], all_farms=False)

    # Still check for a request with higher permissions.
    # This is the same as the get_farm_access dependency above.
    if user_access is not None:
        logger.debug(f"Request has user_access: {user_access}")
        farm_access = user_access

    if api_token_access is not None:
        logger.debug(f"Request has api_token access: {api_token_access}")
        farm_access = api_token_access

    if farm_access is None:
        logger.debug(f"Request has no farm access.")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    return farm_access


def _validate_token(token):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    user_id: int = payload.get("sub", None)
    farm_id = payload.get("farm_id", [])
    all_farms = payload.get("all_farms", False)
    token_scopes = payload.get("scopes", [])
    token_data = TokenData(scopes=token_scopes, user_id=user_id, farm_id=farm_id, all_farms=all_farms)
    return token_data
