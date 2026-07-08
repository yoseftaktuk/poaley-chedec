import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.security import get_current_user
from app.models import User
from app.schemas import PrayerTimeCreate, PrayerTimeResponse, PrayerTimeUpdate
from app.services.dependencies import get_prayer_time_service
from app.services.prayer_time_service import PrayerTimeService

router = APIRouter()


@router.get("", response_model=list[PrayerTimeResponse])
async def list_prayer_times(
    service: PrayerTimeService = Depends(get_prayer_time_service),
) -> list[PrayerTimeResponse]:
    return await service.list_prayer_times()


@router.post("", response_model=PrayerTimeResponse, status_code=status.HTTP_201_CREATED)
async def create_prayer_time(
    payload: PrayerTimeCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: PrayerTimeService = Depends(get_prayer_time_service),
) -> PrayerTimeResponse:
    return await service.create_prayer_time(current_user.id, payload)


@router.put("/{item_id}", response_model=PrayerTimeResponse)
async def update_prayer_time(
    item_id: uuid.UUID,
    payload: PrayerTimeUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: PrayerTimeService = Depends(get_prayer_time_service),
) -> PrayerTimeResponse:
    return await service.update_prayer_time(current_user.id, item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prayer_time(
    item_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    service: PrayerTimeService = Depends(get_prayer_time_service),
) -> None:
    await service.delete_prayer_time(current_user.id, item_id)
