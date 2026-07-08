import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models import PrayerTime
from app.services.utils import get_by_id


@pytest.mark.asyncio
async def test_get_by_id_returns_entity():
    entity_id = uuid.uuid4()
    prayer = PrayerTime(id=entity_id, prayer_name="שחרית", days_of_week=[0], prayer_time="06:00")
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = prayer
    db = AsyncMock()
    db.execute.return_value = mock_result

    result = await get_by_id(db, PrayerTime, entity_id)
    assert result is prayer


@pytest.mark.asyncio
async def test_get_by_id_returns_none():
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    db = AsyncMock()
    db.execute.return_value = mock_result

    result = await get_by_id(db, PrayerTime, uuid.uuid4())
    assert result is None
