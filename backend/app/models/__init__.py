import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import TimestampMixin, new_uuid
from app.core.database import Base


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    token_version: Mapped[int] = mapped_column(Integer, default=0)


class Setting(Base):
    __tablename__ = "settings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    key: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    value: Mapped[dict] = mapped_column(JSONB, default=dict)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class PrayerTime(Base):
    __tablename__ = "prayer_times"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    prayer_name: Mapped[str] = mapped_column(String(100))
    days_of_week: Mapped[list] = mapped_column(JSONB, default=list)
    time_mode: Mapped[str] = mapped_column(String(20), default="fixed")
    prayer_time: Mapped[str | None] = mapped_column(String(50), nullable=True)
    zman_ref: Mapped[str | None] = mapped_column(String(50), nullable=True)
    offset_minutes: Mapped[int] = mapped_column(Integer, default=0)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)


class TorahLesson(Base):
    __tablename__ = "torah_lessons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    lesson_name: Mapped[str] = mapped_column(String(200))
    rabbi_name: Mapped[str] = mapped_column(String(200))
    days_of_week: Mapped[list] = mapped_column(JSONB, default=list)
    lesson_time: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text, default="")
    is_active: Mapped[bool] = mapped_column(default=True)


class Event(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, default="")
    event_date: Mapped[date] = mapped_column(Date)
    event_time: Mapped[str] = mapped_column(String(50))
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    image_public_id: Mapped[str | None] = mapped_column(String(300), nullable=True)
    show_on_homepage: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class GalleryAlbum(Base):
    __tablename__ = "gallery_albums"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, default="")
    cover_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cover_public_id: Mapped[str | None] = mapped_column(String(300), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_published: Mapped[bool] = mapped_column(default=True)


class GalleryImage(Base):
    __tablename__ = "gallery_images"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    album_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    title: Mapped[str] = mapped_column(String(200), default="")
    cloudinary_public_id: Mapped[str] = mapped_column(String(300))
    image_url: Mapped[str] = mapped_column(String(500))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)


class Mikveh(Base):
    __tablename__ = "mikveh"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    general_info: Mapped[str] = mapped_column(Text, default="")
    regulations: Mapped[str] = mapped_column(Text, default="")
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    image_public_id: Mapped[str | None] = mapped_column(String(300), nullable=True)
    avrech_price: Mapped[float] = mapped_column(default=10.0)
    regular_price: Mapped[float] = mapped_column(default=15.0)
    opening_schedules: Mapped[list] = mapped_column(JSONB, default=list)


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    name: Mapped[str] = mapped_column(String(200))
    phone: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(200))
    message: Mapped[str] = mapped_column(Text)
    email_sent: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class BannerMessage(Base):
    __tablename__ = "banner_messages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    message: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(default=True)
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, default=0)
    days_of_week: Mapped[list] = mapped_column(JSONB, default=list)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    action: Mapped[str] = mapped_column(String(50))
    entity_type: Mapped[str] = mapped_column(String(100))
    entity_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    changes: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
