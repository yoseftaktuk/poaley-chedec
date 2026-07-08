from pydantic import BaseModel, ConfigDict, field_validator


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


def _validate_days_of_week(days: list[int], allow_empty: bool = False) -> list[int]:
    from app.services.days_utils import normalize_days_of_week

    return normalize_days_of_week(days, allow_empty=allow_empty)


class OpeningSchedule(BaseModel):
    days_of_week: list[int]
    hours: str

    @field_validator("days_of_week")
    @classmethod
    def validate_days(cls, days: list[int]) -> list[int]:
        return _validate_days_of_week(days)
