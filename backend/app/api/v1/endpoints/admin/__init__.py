from fastapi import APIRouter

from app.api.v1.endpoints.admin import audit_logs, contact_messages

router = APIRouter()
router.include_router(audit_logs.router, prefix="/audit-logs", tags=["admin-audit"])
router.include_router(contact_messages.router, prefix="/contact-messages", tags=["admin-contact"])
