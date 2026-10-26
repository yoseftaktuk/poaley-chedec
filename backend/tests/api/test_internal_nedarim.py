from unittest.mock import AsyncMock, patch

import pytest

from app.core.config import settings


@pytest.fixture
def reconcile_secret(monkeypatch):
    secret = "reconcile-test-secret"
    monkeypatch.setattr(settings, "nedarim_reconcile_secret", secret)
    return secret


async def test_reconcile_unauthorized(client, reconcile_secret):
    response = await client.post(
        "/api/v1/internal/nedarim/reconcile",
        headers={"X-Reconcile-Secret": "wrong"},
    )
    assert response.status_code == 401


async def test_reconcile_ok(client, reconcile_secret):
    with patch(
        "app.api.v1.endpoints.internal_nedarim.DonationReceiptService.reconcile",
        new_callable=AsyncMock,
        return_value=2,
    ):
        response = await client.post(
            "/api/v1/internal/nedarim/reconcile",
            headers={"X-Reconcile-Secret": reconcile_secret},
        )
    assert response.status_code == 200
    assert response.json()["processed"] == 2
