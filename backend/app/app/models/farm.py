from typing import Optional

from pydantic import BaseModel

# Shared properties
class FarmBase(BaseModel):
    farm_name: Optional[str] = None
    url: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_authenticated: Optional[bool] = False

class FarmBaseInDB(FarmBase):
    id: int = None

# Properties to recieve via API on creation
class FarmInCreate(FarmBaseInDB):
    farm_name: str
    url: str
    username: str
    password: str

# Additional properties to return via API
class Farm(FarmBaseInDB):
    pass

# Additional properites stored in DB
class FarmInDB(FarmBaseInDB):
    pass
