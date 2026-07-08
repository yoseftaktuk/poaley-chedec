import uuid
from datetime import UTC, datetime, timedelta

import pytest
from jose import jwt

from app.core.config import settings
from app.core.security import ALGORITHM


@pytest.mark.asyncio
async def test_login_success(client, admin_user):
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "testadmin", "password": "testpass123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client, admin_user):
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "testadmin", "password": "wrongpassword"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_unknown_user(client):
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "nobody", "password": "test"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_requires_auth(client):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_with_valid_token(client, auth_headers, admin_user):
    response = await client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testadmin"


@pytest.mark.asyncio
async def test_me_with_invalid_token(client):
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_with_expired_token(client, admin_user):
    expired_payload = {
        "sub": str(admin_user.id),
        "username": admin_user.username,
        "token_version": admin_user.token_version,
        "type": "access",
        "exp": datetime.now(UTC) - timedelta(hours=1),
    }
    token = jwt.encode(expired_payload, settings.secret_key, algorithm=ALGORITHM)
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout(client):
    response = await client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    assert "התנתקת" in response.json()["message"]


@pytest.mark.asyncio
async def test_refresh_returns_400(client):
    response = await client.post("/api/v1/auth/refresh")
    assert response.status_code == 400
