from datetime import datetime
from typing import Optional

from app.schemas.api_model import APIModel
from app.schemas.farm_info import FarmInfo
from app.schemas.farm_token import FarmToken, FarmTokenBase


# Shared properties
class FarmBase(APIModel):
    farm_name: Optional[str] = None
    url: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[str] = None
    active: Optional[bool] = None
    token: Optional[FarmToken] = None


class FarmBaseInDB(FarmBase):
    id: int = None
    time_created: Optional[datetime] = None
    time_updated: Optional[datetime] = None


# Properties to receive via API on creation
class FarmCreate(FarmBase):
    farm_name: str
    url: str
    scope: Optional[str] = None
    token: Optional[FarmTokenBase] = None


# Properties to receive via API on update
class FarmUpdate(FarmBase):
    token: Optional[FarmTokenBase] = None


# Additional properties to return via API
class Farm(FarmBaseInDB):
    last_accessed: Optional[datetime] = None
    is_authorized: Optional[bool] = None
    scope: Optional[str] = None
    auth_error: Optional[str] = None


# Class that returns farm.json info.
class AllFarmInfo(Farm):
    info: Optional[FarmInfo] = None


# Additional properties stored in DB
class FarmInDB(FarmBaseInDB):
    pass
