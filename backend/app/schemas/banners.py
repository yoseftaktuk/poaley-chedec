import uuid
from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.schemas.base import ORMModel, _validate_days_of_week


class BannerMessageBase(BaseModel):
    message: str
    is_active: bool = True
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    priority: int = 0
    days_of_week: list[int] = Field(default_factory=list)

    @field_validator("days_of_week")
    @classmethod
    def validate_days(cls, days: list[int]) -> list[int]:
        return _validate_days_of_week(days, allow_empty=True)


class BannerMessageCreate(BannerMessageBase):
    pass


class BannerMessageUpdate(BaseModel):
    message: str | None = None
    is_active: bool | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    priority: int | None = None
    days_of_week: list[int] | None = None

    @field_validator("days_of_week")
    @classmethod
    def validate_days(cls, days: list[int] | None) -> list[int] | None:
        if days is None:
            return None
        return _validate_days_of_week(days, allow_empty=True)


class BannerMessageResponse(BannerMessageBase, ORMModel):
    id: uuid.UUID
