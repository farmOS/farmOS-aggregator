from typing import Optional
from datetime import datetime

from app.schemas.api_model import APIModel
from app.schemas.farm_token import FarmTokenBase, FarmToken
from app.schemas.farm_info import FarmInfo

# Shared properties
class FarmBase(APIModel):
    farm_name: Optional[str] = None
    url: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[str] = None
    info: Optional[FarmInfo] = None
    active: Optional[bool] = None

class FarmBaseInDB(FarmBase):
    id: int = None

# Properties to receive via API on creation
class FarmCreate(FarmBase):
    farm_name: str
    url: str
    token: Optional[FarmTokenBase] = None


# Properties to receive via API on update
class FarmUpdate(FarmBase):
    pass


# Additional properties to return via API
class Farm(FarmBaseInDB):
    time_created: Optional[datetime] = None
    time_updated: Optional[datetime] = None
    last_accessed: Optional[datetime] = None
    token: Optional[FarmToken] = None
    is_authorized: Optional[bool] = None
    auth_error: Optional[str] = None


# Additional properties stored in DB
class FarmInDB(FarmBaseInDB):
    pass