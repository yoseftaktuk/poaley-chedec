import uuid
from datetime import date, datetime

from pydantic import BaseModel

from app.schemas.base import ORMModel


class EventBase(BaseModel):
    title: str
    description: str = ""
    event_date: date
    event_time: str
    image_url: str | None = None
    show_on_homepage: bool = False


class EventCreate(EventBase):
    image_public_id: str | None = None


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    event_date: date | None = None
    event_time: str | None = None
    image_url: str | None = None
    image_public_id: str | None = None
    show_on_homepage: bool | None = None


class EventResponse(EventBase, ORMModel):
    id: uuid.UUID
    created_at: datetime
