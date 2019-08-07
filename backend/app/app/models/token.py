from app.models.api_model import APIModel


class Token(APIModel):
    access_token: str
    token_type: str


class TokenPayload(APIModel):
    user_id: int = None
