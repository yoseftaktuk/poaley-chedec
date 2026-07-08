from datetime import date, datetime
from unittest.mock import AsyncMock, patch
from zoneinfo import ZoneInfo

import pytest

from app.services.zmanim_service import (
    apply_offset,
    clear_zmanim_cache,
    fetch_daily_zmanim,
    format_time_hhmm,
)
from app.types.zmanim import ZmanRef


@pytest.fixture(autouse=True)
def _clear_cache():
    clear_zmanim_cache()
    yield
    clear_zmanim_cache()


def test_apply_offset_negative():
    base = datetime(2026, 1, 15, 6, 0, tzinfo=ZoneInfo("Asia/Jerusalem"))
    assert format_time_hhmm(apply_offset(base, -15)) == "05:45"


@pytest.mark.asyncio
async def test_fetch_daily_zmanim_parses_hebcal_response():
    hebcal_payload = {
        "times": {
            "alotHaShachar": "2026-07-08T04:12:00+03:00",
            "sunrise": "2026-07-08T05:42:00+03:00",
            "sunset": "2026-07-08T19:48:00+03:00",
            "tzeit42min": "2026-07-08T20:25:00+03:00",
            "chatzot": "2026-07-08T12:55:00+03:00",
        }
    }

    mock_response = AsyncMock()
    mock_response.raise_for_status = lambda: None
    mock_response.json = lambda: hebcal_payload

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    with patch("app.services.zmanim_service.httpx.AsyncClient", return_value=mock_client):
        result = await fetch_daily_zmanim(date(2026, 7, 8))

    assert ZmanRef.SUNRISE in result
    assert format_time_hhmm(result[ZmanRef.SUNSET]) == "19:48"
    assert format_time_hhmm(result[ZmanRef.TZEIT]) == "20:25"
    assert format_time_hhmm(apply_offset(result[ZmanRef.SUNSET], 20)) == "20:08"

    # second call uses cache
    with patch("app.services.zmanim_service.httpx.AsyncClient") as client_cls:
        await fetch_daily_zmanim(date(2026, 7, 8))
        client_cls.assert_not_called()
