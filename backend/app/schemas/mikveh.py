import uuid

from pydantic import BaseModel, Field

from app.schemas.base import ORMModel, OpeningSchedule


class MikvehBase(BaseModel):
    general_info: str = ""
    regulations: str = ""
    image_url: str | None = None
    avrech_price: float = 10.0
    regular_price: float = 15.0
    opening_schedules: list[OpeningSchedule] = Field(default_factory=list)


class MikvehUpdate(MikvehBase):
    image_public_id: str | None = None


class MikvehResponse(MikvehBase, ORMModel):
    id: uuid.UUID
