import uuid

from pydantic import BaseModel, field_validator

from app.schemas.base import ORMModel, _validate_days_of_week


class TorahLessonBase(BaseModel):
    lesson_name: str
    rabbi_name: str
    days_of_week: list[int]
    lesson_time: str
    description: str = ""
    is_active: bool = True

    @field_validator("days_of_week")
    @classmethod
    def validate_days(cls, days: list[int]) -> list[int]:
        return _validate_days_of_week(days)


class TorahLessonCreate(TorahLessonBase):
    pass


class TorahLessonUpdate(BaseModel):
    lesson_name: str | None = None
    rabbi_name: str | None = None
    days_of_week: list[int] | None = None
    lesson_time: str | None = None
    description: str | None = None
    is_active: bool | None = None

    @field_validator("days_of_week")
    @classmethod
    def validate_days(cls, days: list[int] | None) -> list[int] | None:
        if days is None:
            return None
        return _validate_days_of_week(days)


class TorahLessonResponse(TorahLessonBase, ORMModel):
    id: uuid.UUID
