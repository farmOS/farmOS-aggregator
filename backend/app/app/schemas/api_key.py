from typing import Optional, List
from datetime import datetime

from app.schemas.api_model import APIModel


# API Key Models
class ApiKeyBase(APIModel):
    enabled: Optional[bool] = False
    name: Optional[str] = None
    notes: Optional[str] = None


class ApiKeyInDB(ApiKeyBase):
    id: int
    time_created: Optional[datetime] = None
    key: bytes
    farm_id: Optional[List[int]] = []
    all_farms: Optional[bool] = False
    scopes: Optional[List[str]] = []


class ApiKeyCreate(ApiKeyBase):
    # Only allow these fields to be supplied when creating
    # an API Key. They cannot be modified later.
    farm_id: Optional[List[int]] = []
    all_farms: Optional[bool] = False
    scopes: Optional[List[str]] = []


class ApiKeyUpdate(ApiKeyBase):
    pass


class ApiKey(ApiKeyInDB):
    pass
