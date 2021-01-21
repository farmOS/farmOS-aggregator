import logging
from typing import List
from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.routers.utils.db import get_db
from app.schemas.api_key import ApiKey, ApiKeyCreate, ApiKeyUpdate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=List[ApiKey])
def get_api_keys(db: Session = Depends(get_db)):
    """
    Return all api keys.
    """
    return crud.api_key.get_multi(db)


@router.post("/", response_model=ApiKey)
def create_api_key(
    *,
    db: Session = Depends(get_db),
    key_in: ApiKeyCreate,
):
    """
    Create a new API Key.
    """
    api_key = crud.api_key.create(db, api_key_in=key_in)

    return api_key


@router.put("/{key_id}", response_model=ApiKey)
def update_api_key(
    *,
    db: Session = Depends(get_db),
    key_id: int,
    key_in: ApiKeyUpdate,
):
    """
    Update an existing API Key.

    Only the name, notes, and enabled status can be updated.
    """
    key = crud.api_key.get_by_id(db, key_id=key_id)
    if not key:
        raise HTTPException(
            status_code=404,
            detail="API Key not found.",
        )

    key = crud.api_key.update(db, api_key=key, api_key_in=key_in)
    return key


@router.delete("/{key_id}")
def delete_api_key(
    *,
    db: Session = Depends(get_db),
    key_id: int
):
    """
    Delete an API Key.
    """
    key = crud.api_key.delete(db, key_id=key_id)
    return key
