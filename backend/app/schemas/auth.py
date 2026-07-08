import uuid

from pydantic import BaseModel

from app.schemas.base import ORMModel


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(ORMModel):
    id: uuid.UUID
    username: str
