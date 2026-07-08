import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import ORMModel


class ContactCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    phone: str = Field(min_length=5, max_length=50)
    email: EmailStr
    message: str = Field(min_length=5, max_length=5000)


class ContactMessageResponse(ORMModel):
    id: uuid.UUID
    name: str
    phone: str
    email: str
    message: str
    email_sent: bool
    created_at: datetime
