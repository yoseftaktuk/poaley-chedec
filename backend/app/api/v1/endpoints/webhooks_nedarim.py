"""Nedarim Plus transaction webhook receiver."""

from __future__ import annotations

import json
import logging
import time

from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.schemas.donation_receipts import NedarimWebhookResponse
from app.services.donation_receipt_service import (
    DonationReceiptService,
    process_donation_receipt_background,
)
from app.services.nedarim_hmac import diagnose_nedarim_signature, verify_nedarim_signature

logger = logging.getLogger(__name__)

router = APIRouter()


def _agent_dbg(hypothesis_id: str, message: str, data: dict) -> None:
    # region agent log
    try:
        payload = {
            "sessionId": "fe4a90",
            "hypothesisId": hypothesis_id,
            "location": "webhooks_nedarim.py",
            "message": message,
            "data": data,
            "timestamp": int(time.time() * 1000),
        }
        with open("/Users/natankatz/poaley-chedec/.cursor/debug-fe4a90.log", "a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception:
        pass
    # endregion


@router.post("/transactions", response_model=NedarimWebhookResponse)
async def nedarim_transaction_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    x_nedarim_timestamp: str | None = Header(default=None, alias="X-Nedarim-Timestamp"),
    x_nedarim_signature: str | None = Header(default=None, alias="X-Nedarim-Signature"),
) -> NedarimWebhookResponse:
    started = time.perf_counter()
    # region agent log
    _agent_dbg("A", "webhook entered", {"path": str(request.url.path)})
    # endregion
    raw_body = await request.body()

    if not settings.nedarim_webhook_secret:
        raise HTTPException(status_code=503, detail="Webhook secret not configured")

    valid = verify_nedarim_signature(
        timestamp=x_nedarim_timestamp,
        signature_header=x_nedarim_signature,
        raw_body=raw_body,
        secret=settings.nedarim_webhook_secret,
        max_skew_seconds=settings.nedarim_hmac_max_skew_seconds,
    )
    if not valid:
        diagnosis = diagnose_nedarim_signature(
            timestamp=x_nedarim_timestamp,
            signature_header=x_nedarim_signature,
            raw_body=raw_body,
            secret=settings.nedarim_webhook_secret,
            max_skew_seconds=settings.nedarim_hmac_max_skew_seconds,
        )
        # region agent log
        _agent_dbg(
            "C",
            "signature rejected",
            {"elapsed_ms": round((time.perf_counter() - started) * 1000, 1), **diagnosis},
        )
        # endregion
        logger.warning("nedarim webhook rejected: %s", diagnosis)
        raise HTTPException(status_code=401, detail="Invalid Nedarim signature")
    # region agent log
    _agent_dbg(
        "C",
        "signature accepted",
        {"elapsed_ms": round((time.perf_counter() - started) * 1000, 1), "body_bytes": len(raw_body)},
    )
    # endregion

    try:
        payload = json.loads(raw_body.decode("utf-8") or "{}")
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=400, detail="Invalid JSON body") from exc

    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Invalid JSON object")

    service = DonationReceiptService(db)
    try:
        record, should_process = await service.upsert_from_webhook(payload)
    except ValueError as exc:
        # region agent log
        _agent_dbg(
            "B",
            "upsert rejected",
            {"elapsed_ms": round((time.perf_counter() - started) * 1000, 1)},
        )
        # endregion
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    # region agent log
    _agent_dbg(
        "B",
        "upsert finished",
        {
            "elapsed_ms": round((time.perf_counter() - started) * 1000, 1),
            "should_process": should_process,
            "status": record.status,
        },
    )
    # endregion

    if should_process:
        background_tasks.add_task(process_donation_receipt_background, record.id)

    logger.info(
        "nedarim transaction stored transaction_id=%s status=%s web_doc_id=%s",
        record.transaction_id,
        record.status,
        record.web_doc_id,
    )
    # region agent log
    _agent_dbg(
        "D",
        "returning 200 before background work",
        {
            "elapsed_ms": round((time.perf_counter() - started) * 1000, 1),
            "queued_delivery": should_process,
        },
    )
    # endregion
    return NedarimWebhookResponse(WEBDocID=record.web_doc_id)
