from typing import Optional

from pydantic import BaseModel, Field


# farmOS Server Info to cache
class FarmInfo(BaseModel):
    class Config:
        allow_population_by_field_name = True

    name: str
    url: str
    version: str = Field(alias="api_version")
    user: Optional[dict]
    system_of_measurement: Optional[str]
    resources: Optional[dict]
