import re
import uuid

from pydantic import BaseModel, field_validator, model_validator

from app.schemas.base import ORMModel, _validate_days_of_week
from app.types.zmanim import TimeMode, ZmanRef

_FIXED_TIME_PATTERN = re.compile(r"^\d{1,2}:\d{2}$")


def _validate_fixed_time(value: str | None) -> str | None:
    if value is None:
        return None
    if not _FIXED_TIME_PATTERN.match(value):
        raise ValueError("שעה קבועה חייבת להיות בפורמט HH:MM")
    return value


class PrayerTimeBase(BaseModel):
    prayer_name: str
    days_of_week: list[int]
    time_mode: TimeMode = "fixed"
    prayer_time: str | None = None
    zman_ref: ZmanRef | None = None
    offset_minutes: int = 0
    sort_order: int = 0

    @field_validator("days_of_week")
    @classmethod
    def validate_days(cls, days: list[int]) -> list[int]:
        return _validate_days_of_week(days)

    @field_validator("prayer_time")
    @classmethod
    def validate_prayer_time(cls, value: str | None) -> str | None:
        return _validate_fixed_time(value)

    @model_validator(mode="after")
    def validate_time_mode(self) -> "PrayerTimeBase":
        if self.time_mode == "fixed":
            if not self.prayer_time:
                raise ValueError("שעה קבועה נדרשת במצב fixed")
            self.zman_ref = None
            self.offset_minutes = 0
        elif self.time_mode == "zmanim":
            if self.zman_ref is None:
                raise ValueError("יש לבחור זמן הלכתי במצב zmanim")
            self.prayer_time = None
        return self


class PrayerTimeCreate(PrayerTimeBase):
    pass


class PrayerTimeUpdate(BaseModel):
    prayer_name: str | None = None
    days_of_week: list[int] | None = None
    time_mode: TimeMode | None = None
    prayer_time: str | None = None
    zman_ref: ZmanRef | None = None
    offset_minutes: int | None = None
    sort_order: int | None = None

    @field_validator("days_of_week")
    @classmethod
    def validate_days(cls, days: list[int] | None) -> list[int] | None:
        if days is None:
            return None
        return _validate_days_of_week(days)

    @field_validator("prayer_time")
    @classmethod
    def validate_prayer_time(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _validate_fixed_time(value)


class PrayerTimeResponse(ORMModel):
    id: uuid.UUID
    prayer_name: str
    days_of_week: list[int]
    time_mode: TimeMode
    prayer_time: str
    fixed_time: str | None = None
    zman_ref: ZmanRef | None = None
    offset_minutes: int = 0
    time_definition_label: str | None = None
    sort_order: int = 0
