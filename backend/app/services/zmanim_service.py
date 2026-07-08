import logging
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import httpx

from app.core.config import settings
from app.types.zmanim import HEBCAL_FIELD_MAP, ZmanRef

logger = logging.getLogger(__name__)

_cache: dict[tuple[date, float, float, str], dict[ZmanRef, datetime]] = {}


def clear_zmanim_cache() -> None:
    _cache.clear()


async def fetch_daily_zmanim(
    target_date: date,
    *,
    latitude: float | None = None,
    longitude: float | None = None,
    tzid: str | None = None,
) -> dict[ZmanRef, datetime]:
    lat = latitude if latitude is not None else settings.zmanim_latitude
    lon = longitude if longitude is not None else settings.zmanim_longitude
    timezone_id = tzid or settings.zmanim_tzid
    cache_key = (target_date, lat, lon, timezone_id)

    if cache_key in _cache:
        return _cache[cache_key]

    url = "https://www.hebcal.com/zmanim"
    params = {
        "cfg": "json",
        "latitude": lat,
        "longitude": lon,
        "tzid": timezone_id,
        "date": target_date.isoformat(),
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        payload = response.json()

    times = payload.get("times", {})
    tz = ZoneInfo(timezone_id)
    parsed: dict[ZmanRef, datetime] = {}

    for zman_ref, hebcal_field in HEBCAL_FIELD_MAP.items():
        raw = times.get(hebcal_field)
        if not raw:
            continue
        parsed[zman_ref] = datetime.fromisoformat(raw).astimezone(tz)

    _cache[cache_key] = parsed
    return parsed


def apply_offset(base: datetime, offset_minutes: int) -> datetime:
    return base + timedelta(minutes=offset_minutes)


def format_time_hhmm(dt: datetime) -> str:
    return dt.strftime("%H:%M")
