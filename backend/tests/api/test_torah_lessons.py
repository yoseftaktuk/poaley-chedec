import uuid

import pytest

from app.models import TorahLesson


@pytest.mark.asyncio
async def test_list_torah_lessons_empty(client):
    response = await client.get("/api/v1/torah-lessons")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_torah_lesson(client, auth_headers):
    response = await client.post(
        "/api/v1/torah-lessons",
        headers=auth_headers,
        json={
            "lesson_name": "גמרא",
            "rabbi_name": "הרב",
            "days_of_week": [1, 3],
            "lesson_time": "20:00",
            "description": "שיעור יומי",
        },
    )
    assert response.status_code == 201
    assert response.json()["lesson_name"] == "גמרא"


@pytest.mark.asyncio
async def test_update_torah_lesson_not_found(client, auth_headers):
    response = await client.put(
        f"/api/v1/torah-lessons/{uuid.uuid4()}",
        headers=auth_headers,
        json={"lesson_name": "חומש"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_torah_lesson(client, auth_headers, db_session):
    item = TorahLesson(
        lesson_name="תהילים",
        rabbi_name="הרב",
        days_of_week=[5],
        lesson_time="09:00",
    )
    db_session.add(item)
    await db_session.flush()

    response = await client.delete(
        f"/api/v1/torah-lessons/{item.id}",
        headers=auth_headers,
    )
    assert response.status_code == 204
