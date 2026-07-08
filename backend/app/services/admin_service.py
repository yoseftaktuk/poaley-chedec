from sqlalchemy import select

from app.models import AuditLog, ContactMessage
from app.services.base import BaseService


class AdminService(BaseService):
    async def list_audit_logs(self, limit: int = 200) -> list[AuditLog]:
        result = await self.db.execute(
            select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())

    async def list_contact_messages(self) -> list[ContactMessage]:
        result = await self.db.execute(
            select(ContactMessage).order_by(ContactMessage.created_at.desc())
        )
        return list(result.scalars().all())
