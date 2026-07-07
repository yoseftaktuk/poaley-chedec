import uuid
from datetime import UTC, date, datetime, time
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Event

T = TypeVar("T")


def combine_event_datetime(event_date: date, event_time_str: str) -> datetime:
    parts = event_time_str.split(":")
    hour = int(parts[0]) if parts else 0
    minute = int(parts[1]) if len(parts) > 1 else 0
    return datetime.combine(event_date, time(hour=hour, minute=minute))


def is_event_expired(event: Event) -> bool:
    event_dt = combine_event_datetime(event.event_date, event.event_time)
    return event_dt < datetime.now(UTC).replace(tzinfo=None)


async def get_by_id(db: AsyncSession, model: type[T], entity_id: uuid.UUID) -> T | None:
    result = await db.execute(select(model).where(model.id == entity_id))
    return result.scalar_one_or_none()
