from typing import Optional

from app.models.api_model import APIModel

# Shared properties
class FarmBase(APIModel):
    farm_name: Optional[str] = None
    url: Optional[str] = None
    username: Optional[str] = None

class FarmBaseInDB(FarmBase):
    id: int = None

# Properties to recieve via API on creation
class FarmCreate(FarmBaseInDB):
    farm_name: str
    url: str
    username: str
    password: str

# Properties to receive via API on update
class FarmUpdate(FarmBaseInDB):
    password: Optional[str] = None

# Additional properties to return via API
class Farm(FarmBaseInDB):
    pass

# Additional properites stored in DB
class FarmInDB(FarmBaseInDB):
    pass
