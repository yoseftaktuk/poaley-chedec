import uuid

import pytest

from app.models import PrayerTime


@pytest.mark.asyncio
async def test_list_prayer_times_empty(client):
    response = await client.get("/api/v1/prayer-times")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_prayer_time_requires_auth(client):
    response = await client.post(
        "/api/v1/prayer-times",
        json={
            "prayer_name": "שחרית",
            "days_of_week": [0, 1, 2, 3, 4, 5, 6],
            "prayer_time": "06:30",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_prayer_time_success(client, auth_headers):
    response = await client.post(
        "/api/v1/prayer-times",
        headers=auth_headers,
        json={
            "prayer_name": "שחרית",
            "days_of_week": [0, 1, 2, 3, 4, 5, 6],
            "prayer_time": "06:30",
            "sort_order": 1,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["prayer_name"] == "שחרית"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_prayer_time_validation_error(client, auth_headers):
    response = await client.post(
        "/api/v1/prayer-times",
        headers=auth_headers,
        json={
            "prayer_name": "שחרית",
            "days_of_week": [],
            "prayer_time": "06:30",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_prayer_time(client, auth_headers, db_session):
    item = PrayerTime(
        prayer_name="מנחה",
        days_of_week=[0, 1, 2, 3, 4],
        prayer_time="13:00",
    )
    db_session.add(item)
    await db_session.flush()

    response = await client.put(
        f"/api/v1/prayer-times/{item.id}",
        headers=auth_headers,
        json={"prayer_time": "13:30"},
    )
    assert response.status_code == 200
    assert response.json()["prayer_time"] == "13:30"


@pytest.mark.asyncio
async def test_update_prayer_time_not_found(client, auth_headers):
    response = await client.put(
        f"/api/v1/prayer-times/{uuid.uuid4()}",
        headers=auth_headers,
        json={"prayer_time": "13:30"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_prayer_time(client, auth_headers, db_session):
    item = PrayerTime(
        prayer_name="ערבית",
        days_of_week=[0, 1, 2, 3, 4, 5, 6],
        prayer_time="19:00",
    )
    db_session.add(item)
    await db_session.flush()

    response = await client.delete(
        f"/api/v1/prayer-times/{item.id}",
        headers=auth_headers,
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_prayer_time_not_found(client, auth_headers):
    response = await client.delete(
        f"/api/v1/prayer-times/{uuid.uuid4()}",
        headers=auth_headers,
    )
    assert response.status_code == 404
