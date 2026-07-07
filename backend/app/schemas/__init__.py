import json
import uuid
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# Auth
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(ORMModel):
    id: uuid.UUID
    username: str


class UploadImageResponse(BaseModel):
    url: str
    public_id: str


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


# Prayer Times
class PrayerTimeBase(BaseModel):
    prayer_name: str
    days_of_week: list[int]
    prayer_time: str
    sort_order: int = 0

    @field_validator("days_of_week")
    @classmethod
    def validate_days(cls, days: list[int]) -> list[int]:
        return _validate_days_of_week(days)


class PrayerTimeCreate(PrayerTimeBase):
    pass


class PrayerTimeUpdate(BaseModel):
    prayer_name: str | None = None
    days_of_week: list[int] | None = None
    prayer_time: str | None = None
    sort_order: int | None = None

    @field_validator("days_of_week")
    @classmethod
    def validate_days(cls, days: list[int] | None) -> list[int] | None:
        if days is None:
            return None
        return _validate_days_of_week(days)


class PrayerTimeResponse(PrayerTimeBase, ORMModel):
    id: uuid.UUID


# Torah Lessons
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


# Events
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


# Gallery
class GalleryAlbumBase(BaseModel):
    title: str
    description: str = ""
    cover_image_url: str | None = None
    sort_order: int = 0
    is_published: bool = True


class GalleryAlbumCreate(GalleryAlbumBase):
    cover_public_id: str | None = None


class GalleryAlbumUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    cover_image_url: str | None = None
    cover_public_id: str | None = None
    sort_order: int | None = None
    is_published: bool | None = None


class GalleryAlbumResponse(GalleryAlbumBase, ORMModel):
    id: uuid.UUID


class GalleryImageBase(BaseModel):
    album_id: uuid.UUID
    title: str = ""
    cloudinary_public_id: str
    image_url: str
    sort_order: int = 0


class GalleryImageCreate(GalleryImageBase):
    pass


class GalleryImageUpdate(BaseModel):
    title: str | None = None
    sort_order: int | None = None


class GalleryImageResponse(GalleryImageBase, ORMModel):
    id: uuid.UUID


# Mikveh
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


# Contact
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


# Banners
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


# Settings
class SettingUpdate(BaseModel):
    value: dict[str, Any]


class SettingResponse(BaseModel):
    key: str
    value: dict[str, Any]


# Audit
class AuditLogResponse(ORMModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    action: str
    entity_type: str
    entity_id: uuid.UUID | None
    changes: dict[str, Any]
    created_at: datetime


# Homepage aggregate
class HomepageResponse(BaseModel):
    settings: dict[str, Any]
    prayer_times: list[PrayerTimeResponse]
    torah_lessons: list[TorahLessonResponse]
    events: list[EventResponse]
    banners: list[BannerMessageResponse]
