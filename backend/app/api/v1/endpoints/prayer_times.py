import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.audit import log_audit
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import PrayerTime, User
from app.schemas import PrayerTimeCreate, PrayerTimeResponse, PrayerTimeUpdate
from app.services.days_utils import first_day_of_week
from app.services.prayer_times_api import (
    apply_prayer_time_update,
    prayer_time_from_create,
    to_prayer_time_response,
    to_prayer_time_responses,
)
from app.services.utils import get_by_id

router = APIRouter()


def _sort_by_first_day(items: list[PrayerTime]) -> list[PrayerTime]:
    return sorted(items, key=lambda item: first_day_of_week(item.days_of_week or []))


@router.get("", response_model=list[PrayerTimeResponse])
async def list_prayer_times(db: AsyncSession = Depends(get_db)) -> list[PrayerTimeResponse]:
    result = await db.execute(select(PrayerTime).order_by(PrayerTime.sort_order))
    items = _sort_by_first_day(list(result.scalars().all()))
    return await to_prayer_time_responses(items)


@router.post("", response_model=PrayerTimeResponse, status_code=status.HTTP_201_CREATED)
async def create_prayer_time(
    payload: PrayerTimeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> PrayerTimeResponse:
    item = prayer_time_from_create(payload)
    db.add(item)
    await log_audit(db, user_id=current_user.id, action="create", entity_type="prayer_time", changes=payload.model_dump())
    await db.commit()
    await db.refresh(item)
    return await to_prayer_time_response(item)


@router.put("/{item_id}", response_model=PrayerTimeResponse)
async def update_prayer_time(
    item_id: uuid.UUID,
    payload: PrayerTimeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> PrayerTimeResponse:
    item = await get_by_id(db, PrayerTime, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="לא נמצא")
    apply_prayer_time_update(item, payload)
    await log_audit(db, user_id=current_user.id, action="update", entity_type="prayer_time", entity_id=item.id)
    await db.commit()
    await db.refresh(item)
    return await to_prayer_time_response(item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prayer_time(
    item_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> None:
    item = await get_by_id(db, PrayerTime, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="לא נמצא")
    await log_audit(db, user_id=current_user.id, action="delete", entity_type="prayer_time", entity_id=item.id)
    await db.delete(item)
    await db.commit()
