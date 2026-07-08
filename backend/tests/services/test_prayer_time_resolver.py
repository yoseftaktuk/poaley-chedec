from datetime import date, datetime, timedelta
from unittest.mock import AsyncMock, patch
from zoneinfo import ZoneInfo

import pytest

from app.services.prayer_time_resolver import (
    format_time_definition_label,
    pick_target_date,
    resolve_prayer_time,
)
from app.services.zmanim_service import apply_offset, clear_zmanim_cache, format_time_hhmm
from app.types.zmanim import ZmanRef


@pytest.fixture(autouse=True)
def _clear_cache():
    clear_zmanim_cache()
    yield
    clear_zmanim_cache()


def test_apply_offset():
    base = datetime(2026, 7, 8, 19, 0, tzinfo=ZoneInfo("Asia/Jerusalem"))
    result = apply_offset(base, 20)
    assert result.hour == 19 and result.minute == 20


def test_format_time_hhmm():
    dt = datetime(2026, 7, 8, 6, 5, tzinfo=ZoneInfo("Asia/Jerusalem"))
    assert format_time_hhmm(dt) == "06:05"


def test_pick_target_date_when_today_matches():
    # 2026-07-08 is Wednesday (weekday 2)
    today = date(2026, 7, 8)
    assert pick_target_date([2, 4], today) == today


def test_pick_target_date_next_occurrence():
    today = date(2026, 7, 8)
    expected = today
    for offset in range(1, 8):
        candidate = today + timedelta(days=offset)
        if candidate.weekday() == 0:
            expected = candidate
            break
    assert pick_target_date([0], today) == expected


def test_format_time_definition_label():
    assert format_time_definition_label(ZmanRef.SUNSET, 20) == "שקיעה + 20 דק'"
    assert format_time_definition_label(ZmanRef.SUNRISE, 0) == "זריחה"
    assert format_time_definition_label(ZmanRef.SUNSET, -10) == "שקיעה - 10 דק'"


@pytest.mark.asyncio
async def test_resolve_fixed_prayer_time():
    from app.models import PrayerTime

    item = PrayerTime(
        prayer_name="שחרית",
        days_of_week=[0],
        time_mode="fixed",
        prayer_time="06:30",
    )
    assert await resolve_prayer_time(item) == "06:30"


@pytest.mark.asyncio
async def test_resolve_zmanim_prayer_time():
    from app.models import PrayerTime

    item = PrayerTime(
        prayer_name="מעריב",
        days_of_week=[0, 1, 2, 3, 4, 5, 6],
        time_mode="zmanim",
        zman_ref="sunset",
        offset_minutes=20,
    )
    sunset = datetime(2026, 7, 8, 19, 30, tzinfo=ZoneInfo("Asia/Jerusalem"))
    mock_daily = {ZmanRef.SUNSET: sunset}

    with patch(
        "app.services.prayer_time_resolver.fetch_daily_zmanim",
        new=AsyncMock(return_value=mock_daily),
    ):
        result = await resolve_prayer_time(item, target_date=date(2026, 7, 8))

    assert result == "19:50"
