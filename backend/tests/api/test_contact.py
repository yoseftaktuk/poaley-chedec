import pytest


@pytest.mark.asyncio
async def test_submit_contact_success(client):
    response = await client.post(
        "/api/v1/contact",
        json={
            "name": "ישראל ישראלי",
            "phone": "0501234567",
            "email": "test@example.com",
            "message": "שלום, הודעה לבדיקה",
        },
    )
    assert response.status_code == 201
    assert "נשלחה" in response.json()["message"]


@pytest.mark.asyncio
async def test_submit_contact_validation_error(client):
    response = await client.post(
        "/api/v1/contact",
        json={
            "name": "A",
            "phone": "05",
            "email": "bad",
            "message": "hi",
        },
    )
    assert response.status_code == 422
