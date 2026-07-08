from typing import Annotated

from fastapi import APIRouter, Depends, Request
from app.core.limiter import limiter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.audit import log_audit
from app.core.database import get_db
from app.core.sanitize import sanitize_text
from app.models import ContactMessage
from app.schemas import ContactCreate, MessageResponse
from app.services.seed import send_contact_email

router = APIRouter()


@router.post("", response_model=MessageResponse, status_code=201)
@limiter.limit("5/hour")
async def submit_contact(
    request: Request,
    payload: ContactCreate,
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    email_sent = await send_contact_email(payload.name, payload.phone, str(payload.email), payload.message)
    message = ContactMessage(
        name=sanitize_text(payload.name),
        phone=sanitize_text(payload.phone),
        email=str(payload.email),
        message=sanitize_text(payload.message),
        email_sent=email_sent,
    )
    db.add(message)
    await log_audit(db, user_id=None, action="create", entity_type="contact_message", entity_id=message.id)
    await db.commit()
    return MessageResponse(message="ההודעה נשלחה בהצלחה")

