"""Internal Nedarim reconcile endpoint (cron / ops)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.schemas.donation_receipts import ReconcileResponse
from app.services.donation_receipt_service import DonationReceiptService

router = APIRouter()


@router.post("/reconcile", response_model=ReconcileResponse)
async def reconcile_nedarim_donations(
    db: AsyncSession = Depends(get_db),
    x_reconcile_secret: str | None = Header(default=None, alias="X-Reconcile-Secret"),
) -> ReconcileResponse:
    if not settings.nedarim_reconcile_secret:
        raise HTTPException(status_code=503, detail="Reconcile secret not configured")
    if x_reconcile_secret != settings.nedarim_reconcile_secret:
        raise HTTPException(status_code=401, detail="Unauthorized")

    service = DonationReceiptService(db)
    processed = await service.reconcile()
    return ReconcileResponse(processed=processed, message="reconcile completed")
