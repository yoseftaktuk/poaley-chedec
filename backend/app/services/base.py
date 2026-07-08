import uuid
from typing import Any, TypeVar

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.audit import log_audit
from app.services.utils import get_by_id

T = TypeVar("T")


class BaseService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_or_404(self, model: type[T], entity_id: uuid.UUID) -> T:
        item = await get_by_id(self.db, model, entity_id)
        if not item:
            raise HTTPException(status_code=404, detail="לא נמצא")
        return item

    async def create_audited(
        self,
        item: T,
        *,
        user_id: uuid.UUID,
        entity_type: str,
        changes: dict[str, Any] | None = None,
        action: str = "create",
    ) -> T:
        self.db.add(item)
        await log_audit(
            self.db,
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            changes=changes,
        )
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def commit_audited_update(
        self,
        item: T,
        *,
        user_id: uuid.UUID,
        entity_type: str,
    ) -> T:
        await log_audit(
            self.db,
            user_id=user_id,
            action="update",
            entity_type=entity_type,
            entity_id=item.id,
        )
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update_audited(
        self,
        item: T,
        *,
        user_id: uuid.UUID,
        entity_type: str,
        updates: dict[str, Any],
    ) -> T:
        for key, value in updates.items():
            setattr(item, key, value)
        await log_audit(
            self.db,
            user_id=user_id,
            action="update",
            entity_type=entity_type,
            entity_id=item.id,
        )
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def delete_audited(
        self,
        item: T,
        *,
        user_id: uuid.UUID,
        entity_type: str,
    ) -> None:
        await log_audit(
            self.db,
            user_id=user_id,
            action="delete",
            entity_type=entity_type,
            entity_id=item.id,
        )
        await self.db.delete(item)
        await self.db.commit()
