import pytest


@pytest.mark.asyncio
async def test_audit_logs_requires_auth(client):
    response = await client.get("/api/v1/admin/audit-logs")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_audit_logs_with_auth(client, auth_headers):
    response = await client.get("/api/v1/admin/audit-logs", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_contact_messages_requires_auth(client):
    response = await client.get("/api/v1/admin/contact-messages")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_contact_messages_with_auth(client, auth_headers):
    response = await client.get("/api/v1/admin/contact-messages", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_upload_requires_auth(client):
    response = await client.post("/api/v1/uploads/image")
    assert response.status_code == 401
