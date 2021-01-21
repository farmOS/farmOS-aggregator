from typing import Optional

from pydantic import BaseModel, Field


# farmOS Server Info to cache
class FarmInfo(BaseModel):
    name: str
    url: str
    api_version: str = Field(alias="version")
    user: Optional[dict]
    system_of_measurement: Optional[str]
    resources: Optional[dict]

