from typing import List

from app.models.api_model import APIModel


class Token(APIModel):
    access_token: str
    token_type: str


class TokenData(APIModel):
    user_id: int = None
    scopes: List[str] = []
    farm_id: List[int] = []


class FarmAccess(APIModel):
    user_id: int = None
    scopes: List[str] = []
    farm_id_list: List[int] = []
    all_farms: bool = False

    def can_access_farm(self, farm_id):
        if self.all_farms:
            return True
        else:
            return farm_id in self.farm_id_list
