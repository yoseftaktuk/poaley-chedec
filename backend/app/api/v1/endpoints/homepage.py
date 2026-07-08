from datetime import UTC, datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import BannerMessage, Event, PrayerTime, TorahLesson
from app.schemas import HomepageResponse, HomepageSettingsSnapshot
from app.services.days_utils import first_day_of_week, is_active_on_weekday
from app.services.prayer_time_service import PrayerTimeService
from app.services.seed import get_setting
from app.services.utils import is_event_expired

router = APIRouter()


def _sort_by_first_day(items: list) -> list:
    return sorted(items, key=lambda item: first_day_of_week(item.days_of_week or []))


@router.get("/homepage", response_model=HomepageResponse)
async def get_homepage(db: AsyncSession = Depends(get_db)) -> HomepageResponse:
    prayer_result = await db.execute(select(PrayerTime).order_by(PrayerTime.sort_order))
    lessons_result = await db.execute(
        select(TorahLesson).where(TorahLesson.is_active.is_(True))
    )
    events_result = await db.execute(select(Event).order_by(Event.event_date))
    now = datetime.now(UTC)
    banners_result = await db.execute(
        select(BannerMessage)
        .where(BannerMessage.is_active.is_(True))
        .order_by(BannerMessage.priority.desc())
    )

    events = [e for e in events_result.scalars().all() if not is_event_expired(e)]
    homepage_events = [e for e in events if e.show_on_homepage]

    banners = []
    for banner in banners_result.scalars().all():
        if banner.starts_at and banner.starts_at > now:
            continue
        if banner.ends_at and banner.ends_at < now:
            continue
        if not is_active_on_weekday(banner.days_of_week or []):
            continue
        banners.append(banner)

    settings = HomepageSettingsSnapshot(
        homepage=await get_setting(db, "homepage"),
        contact=await get_setting(db, "contact"),
        donation=await get_setting(db, "donation"),
        site=await get_setting(db, "site"),
    )

    prayer_items = _sort_by_first_day(list(prayer_result.scalars().all()))
    resolved_prayer_times = await PrayerTimeService(db).to_prayer_time_responses(prayer_items)

    return HomepageResponse(
        settings=settings,
        prayer_times=resolved_prayer_times,
        torah_lessons=_sort_by_first_day(list(lessons_result.scalars().all())),
        events=homepage_events,
        banners=banners,
    )
