from fastapi import HTTPException

from app.models import PrayerTime
from app.schemas import PrayerTimeCreate, PrayerTimeResponse, PrayerTimeUpdate
from app.services.prayer_time_resolver import enrich_prayer_time


def _validate_merged_prayer_time(item: PrayerTime) -> None:
    mode = item.time_mode or "fixed"
    if mode == "fixed":
        if not item.prayer_time:
            raise HTTPException(status_code=422, detail="שעה קבועה נדרשת במצב fixed")
        item.zman_ref = None
        item.offset_minutes = 0
    elif mode == "zmanim":
        if not item.zman_ref:
            raise HTTPException(status_code=422, detail="יש לבחור זמן הלכתי במצב zmanim")
        item.prayer_time = None


def apply_prayer_time_update(item: PrayerTime, payload: PrayerTimeUpdate) -> None:
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    _validate_merged_prayer_time(item)


async def to_prayer_time_response(item: PrayerTime) -> PrayerTimeResponse:
    return await enrich_prayer_time(item)


async def to_prayer_time_responses(items: list[PrayerTime]) -> list[PrayerTimeResponse]:
    return [await to_prayer_time_response(item) for item in items]


def prayer_time_from_create(payload: PrayerTimeCreate) -> PrayerTime:
    return PrayerTime(**payload.model_dump())
