import logging
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from app.core.config import settings
from app.models import PrayerTime
from app.schemas import PrayerTimeResponse
from app.services.zmanim_service import apply_offset, fetch_daily_zmanim, format_time_hhmm
from app.types.zmanim import ZMAN_REF_LABELS_HE, TimeMode, ZmanRef

logger = logging.getLogger(__name__)

UNRESOLVED_TIME = "—"


def pick_target_date(days_of_week: list[int], today: date | None = None) -> date:
    today = today or datetime.now(ZoneInfo(settings.zmanim_tzid)).date()
    normalized = sorted(set(days_of_week))
    if not normalized:
        return today
    if today.weekday() in normalized:
        return today
    for offset in range(1, 8):
        candidate = today + timedelta(days=offset)
        if candidate.weekday() in normalized:
            return candidate
    return today


def format_time_definition_label(zman_ref: ZmanRef | str | None, offset_minutes: int) -> str | None:
    if not zman_ref:
        return None
    try:
        ref = ZmanRef(zman_ref)
    except ValueError:
        return None
    label = ZMAN_REF_LABELS_HE.get(ref, str(zman_ref))
    if offset_minutes == 0:
        return label
    if offset_minutes > 0:
        return f"{label} + {offset_minutes} דק'"
    return f"{label} - {abs(offset_minutes)} דק'"


async def resolve_prayer_time(item: PrayerTime, target_date: date | None = None) -> str:
    mode = getattr(item, "time_mode", None) or "fixed"
    if mode == "fixed":
        return item.prayer_time or UNRESOLVED_TIME

    zman_ref_raw = getattr(item, "zman_ref", None)
    if not zman_ref_raw:
        return UNRESOLVED_TIME

    try:
        zman_ref = ZmanRef(zman_ref_raw)
    except ValueError:
        logger.warning("Unknown zman_ref %s for prayer %s", zman_ref_raw, item.id)
        return UNRESOLVED_TIME

    offset = getattr(item, "offset_minutes", 0) or 0
    resolve_date = target_date or pick_target_date(item.days_of_week or [])

    try:
        daily = await fetch_daily_zmanim(resolve_date)
        base = daily.get(zman_ref)
        if base is None:
            return UNRESOLVED_TIME
        return format_time_hhmm(apply_offset(base, offset))
    except Exception:
        logger.exception("Failed to resolve zmanim prayer time for %s", item.id)
        return UNRESOLVED_TIME


async def enrich_prayer_time(item: PrayerTime, target_date: date | None = None) -> PrayerTimeResponse:
    mode: TimeMode = getattr(item, "time_mode", None) or "fixed"
    zman_ref = getattr(item, "zman_ref", None)
    offset = getattr(item, "offset_minutes", 0) or 0
    resolved = await resolve_prayer_time(item, target_date)

    return PrayerTimeResponse(
        id=item.id,
        prayer_name=item.prayer_name,
        days_of_week=item.days_of_week or [],
        time_mode=mode,
        prayer_time=resolved,
        fixed_time=item.prayer_time if mode == "fixed" else None,
        zman_ref=zman_ref,
        offset_minutes=offset,
        time_definition_label=format_time_definition_label(zman_ref, offset)
        if mode == "zmanim"
        else None,
        sort_order=item.sort_order,
    )
