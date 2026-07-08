import uuid

import pytest

from app.models import GalleryAlbum, Mikveh, Setting
from app.services.seed import DEFAULT_SETTINGS


@pytest.mark.asyncio
async def test_list_gallery_albums_empty(client):
    response = await client.get("/api/v1/gallery/albums")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_all_albums_requires_auth(client):
    response = await client.get("/api/v1/gallery/albums?all=true")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_gallery_album(client, auth_headers):
    response = await client.post(
        "/api/v1/gallery/albums",
        headers=auth_headers,
        json={"title": "אלבום בדיקה", "description": "תיאור"},
    )
    assert response.status_code == 201
    assert response.json()["title"] == "אלבום בדיקה"


@pytest.mark.asyncio
async def test_get_mikveh_not_found_when_empty(client):
    response = await client.get("/api/v1/mikveh")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_mikveh(client, auth_headers, db_session):
    mikveh = Mikveh(
        general_info="מידע",
        regulations="תקנון",
        avrech_price=10,
        regular_price=15,
        opening_schedules=[],
    )
    db_session.add(mikveh)
    await db_session.flush()

    response = await client.put(
        "/api/v1/mikveh",
        headers=auth_headers,
        json={
            "general_info": "מידע מעודכן",
            "regulations": "תקנון",
            "avrech_price": 12,
            "regular_price": 18,
            "opening_schedules": [],
        },
    )
    assert response.status_code == 200
    assert response.json()["general_info"] == "מידע מעודכן"


@pytest.mark.asyncio
async def test_public_settings(client, db_session):
    for key, value in DEFAULT_SETTINGS.items():
        db_session.add(Setting(key=key, value=value))
    await db_session.flush()

    response = await client.get("/api/v1/settings/public")
    assert response.status_code == 200
    data = response.json()
    assert "contact" in data
    assert "homepage" in data


@pytest.mark.asyncio
async def test_admin_settings_requires_auth(client):
    response = await client.get("/api/v1/settings/homepage")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_admin_settings_with_auth(client, auth_headers, db_session):
    db_session.add(Setting(key="homepage", value=DEFAULT_SETTINGS["homepage"]))
    await db_session.flush()

    response = await client.get("/api/v1/settings/homepage", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["key"] == "homepage"
