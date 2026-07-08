import uuid
from datetime import date

import pytest

from app.models import Event


@pytest.mark.asyncio
async def test_list_events_empty(client):
    response = await client.get("/api/v1/events")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_event(client, auth_headers):
    response = await client.post(
        "/api/v1/events",
        headers=auth_headers,
        json={
            "title": "אירוע קהילתי",
            "description": "תיאור",
            "event_date": "2099-06-15",
            "event_time": "18:00",
            "show_on_homepage": True,
        },
    )
    assert response.status_code == 201
    assert response.json()["title"] == "אירוע קהילתי"


@pytest.mark.asyncio
async def test_list_events_excludes_expired(client, db_session):
    past = Event(
        title="Past",
        event_date=date(2020, 1, 1),
        event_time="10:00",
    )
    future = Event(
        title="Future",
        event_date=date(2099, 6, 15),
        event_time="18:00",
    )
    db_session.add_all([past, future])
    await db_session.flush()

    response = await client.get("/api/v1/events")
    assert response.status_code == 200
    titles = [e["title"] for e in response.json()]
    assert "Future" in titles
    assert "Past" not in titles


@pytest.mark.asyncio
async def test_delete_event_not_found(client, auth_headers):
    response = await client.delete(
        f"/api/v1/events/{uuid.uuid4()}",
        headers=auth_headers,
    )
    assert response.status_code == 404
