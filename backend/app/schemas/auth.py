from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario_id: int
    username: str
    rol: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    rol: Optional[str] = None
