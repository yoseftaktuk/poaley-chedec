"""Verify Nedarim Plus webhook HMAC signatures."""

from __future__ import annotations

import hashlib
import hmac
import time


def verify_nedarim_signature(
    *,
    timestamp: str | None,
    signature_header: str | None,
    raw_body: bytes,
    secret: str,
    max_skew_seconds: int = 300,
    now: float | None = None,
) -> bool:
    """Return True when X-Nedarim-* headers match HMAC-SHA256(timestamp + '.' + body)."""
    if not secret or not timestamp or not signature_header:
        return False

    try:
        ts = int(timestamp)
    except ValueError:
        return False

    current = time.time() if now is None else now
    if abs(current - ts) > max_skew_seconds:
        return False

    provided = signature_header.strip().removeprefix("v1=").strip().lower()
    if not provided:
        return False

    message = f"{timestamp}.".encode("utf-8") + raw_body
    expected = hmac.new(secret.encode("utf-8"), message, hashlib.sha256).hexdigest()
    if len(provided) != len(expected):
        return False
    return hmac.compare_digest(expected, provided)
