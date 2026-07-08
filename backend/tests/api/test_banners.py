import pytest

from app.models import BannerMessage


@pytest.mark.asyncio
async def test_list_active_banners_empty(client):
    response = await client.get("/api/v1/banners/active")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_banners_requires_auth(client):
    response = await client.get("/api/v1/banners")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_banner(client, auth_headers):
    response = await client.post(
        "/api/v1/banners",
        headers=auth_headers,
        json={"message": "הודעה חשובה", "is_active": True, "priority": 1},
    )
    assert response.status_code == 201
    assert response.json()["message"] == "הודעה חשובה"


@pytest.mark.asyncio
async def test_active_banners_returns_active(client, auth_headers, db_session):
    banner = BannerMessage(message="פעיל", is_active=True, priority=1)
    db_session.add(banner)
    await db_session.flush()

    response = await client.get("/api/v1/banners/active")
    assert response.status_code == 200
    assert len(response.json()) >= 1
