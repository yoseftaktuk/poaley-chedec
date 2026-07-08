import pytest

from app.models import Setting
from app.services.seed import DEFAULT_SETTINGS


@pytest.mark.asyncio
async def test_get_homepage(client, db_session):
    for key, value in DEFAULT_SETTINGS.items():
        db_session.add(Setting(key=key, value=value))
    await db_session.flush()

    response = await client.get("/api/v1/homepage")
    assert response.status_code == 200
    data = response.json()
    assert "settings" in data
    assert "prayer_times" in data
    assert "torah_lessons" in data
    assert "events" in data
    assert "banners" in data
