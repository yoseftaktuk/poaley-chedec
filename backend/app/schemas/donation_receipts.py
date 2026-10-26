from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class NedarimWebhookResponse(BaseModel):
    WEBDocID: int = Field(description="Internal numeric id for Nedarim CallBackId cross-ref")


class DonationReceiptOut(BaseModel):
    id: UUID
    transaction_id: str
    status: str
    channel: str | None = None
    receipt_url: str | None = None
    send_attempts: int = 0
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class ReconcileResponse(BaseModel):
    processed: int
    message: str
