from typing import List
from datetime import datetime, timedelta

import jwt

from app.core import config

ALGORITHM = "HS256"


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_farm_api_token(farm_id: List[int], scopes: List[str]):
    delta = timedelta(hours=config.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    encoded_jwt = jwt.encode(
        {
            'exp': expires.timestamp(),
            'nbf': now.timestamp(),
            "sub": 0,
            "farm_id": farm_id,
            "scopes": scopes,
        },
        config.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt
