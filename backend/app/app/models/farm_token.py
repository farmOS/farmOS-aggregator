from typing import Optional

from app.models.api_model import APIModel

# Farm Token Models
class FarmTokenBase(APIModel):
    farm_id: int
    access_token: Optional[str] = None
    expires_in: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_at: Optional[str] = None


class FarmTokenCreate(FarmTokenBase):
    pass


class FarmToken(FarmTokenBase):
    id: int


class FarmTokenUpdate(FarmToken):
    pass

class FarmAuthorizationParams(APIModel):
    grant_type: str
    code: str
    state: str
    client_id: str
    client_secret: Optional[str]
    redirect_uri: Optional[str]