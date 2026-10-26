"""Nedarim Plus API client for receipts and history."""

from __future__ import annotations

import logging
import re
from typing import Any
from urllib.parse import urlencode

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

EZCOUNT_RECEIPT_BASE = "https://files.ezcount.co.il/front/documents/get"
_UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)


def is_uuid(value: str) -> bool:
    return bool(_UUID_RE.match(value.strip()))


def ezcount_url(document_id: str) -> str:
    return f"{EZCOUNT_RECEIPT_BASE}/{document_id.strip()}"


def resolve_receipt_url_from_webhook(
    *,
    receipt_data: str | None,
    receipt_created: str | None,
) -> str | None:
    """Resolve a receipt URL from webhook fields without calling Nedarim."""
    raw = (receipt_data or "").strip()
    if not raw:
        return None
    if raw.startswith("http://") or raw.startswith("https://"):
        return raw
    if is_uuid(raw):
        return ezcount_url(raw)

    created = (receipt_created or "").strip().lower()
    if created in {"1", "true", "yes"} and raw:
        # Non-UUID document id still usable for Ezcount
        return ezcount_url(raw)
    return None


async def show_invoice(transaction_id: str) -> str | None:
    """Call ShowInvoice; return receipt URL from Message when Result=OK."""
    if not settings.nedarim_api_password:
        logger.warning("Nedarim API password not configured; skipping ShowInvoice")
        return None

    params = {
        "Action": "ShowInvoice",
        "MosadId": settings.nedarim_mosad_id,
        "ApiPassword": settings.nedarim_api_password,
        "TransactionId": transaction_id,
    }
    url = f"https://matara.pro/nedarimplus/Reports/Tamal3.aspx?{urlencode(params)}"

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
    except Exception:
        logger.exception("ShowInvoice failed for transaction_id=%s", transaction_id)
        return None

    if data.get("Result") != "OK":
        logger.info(
            "ShowInvoice not OK for transaction_id=%s message=%s",
            transaction_id,
            str(data.get("Message", ""))[:120],
        )
        return None

    message = str(data.get("Message") or "").strip()
    if message.startswith("http"):
        return message
    return None


async def get_history_after(last_id: int, *, max_id: int = 100) -> list[dict[str, Any]]:
    """Fetch transaction history rows with LastId / MaxId."""
    if not settings.nedarim_api_password:
        logger.warning("Nedarim API password not configured; skipping GetHistoryJson")
        return []

    params = {
        "Action": "GetHistoryJson",
        "MosadId": settings.nedarim_mosad_id,
        "ApiPassword": settings.nedarim_api_password,
        "LastId": str(last_id),
        "MaxId": str(max_id),
    }
    url = f"https://matara.pro/nedarimplus/Reports/Manage3.aspx?{urlencode(params)}"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
    except Exception:
        logger.exception("GetHistoryJson failed last_id=%s", last_id)
        return []

    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("History", "Rows", "Data", "data"):
            rows = data.get(key)
            if isinstance(rows, list):
                return rows
        if data.get("Result") == "Error":
            logger.info("GetHistoryJson error: %s", str(data.get("Message", ""))[:120])
            return []
    return []


def history_row_receipt_url(row: dict[str, Any]) -> str | None:
    invoice = str(row.get("InvoiceData2") or "").strip()
    if invoice:
        if invoice.startswith("http"):
            return invoice
        return ezcount_url(invoice)
    return resolve_receipt_url_from_webhook(
        receipt_data=str(row.get("ReceiptData") or "") or None,
        receipt_created=str(row.get("ReceiptCreated") or "") or None,
    )
