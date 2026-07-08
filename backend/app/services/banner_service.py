import uuid
from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy import select

from app.models import BannerMessage
from app.schemas import BannerMessageCreate, BannerMessageUpdate
from app.services.base import BaseService
from app.services.days_utils import is_active_on_weekday


class BannerService(BaseService):
    @staticmethod
    def _filter_active_banners(banners: list[BannerMessage], now: datetime) -> list[BannerMessage]:
        result = []
        for banner in banners:
            if banner.starts_at and banner.starts_at > now:
                continue
            if banner.ends_at and banner.ends_at < now:
                continue
            if not is_active_on_weekday(banner.days_of_week or []):
                continue
            result.append(banner)
        return result

    async def list_active_banners(self) -> list[BannerMessage]:
        now = datetime.now(UTC)
        result = await self.db.execute(
            select(BannerMessage).where(BannerMessage.is_active.is_(True)).order_by(BannerMessage.priority.desc())
        )
        return self._filter_active_banners(list(result.scalars().all()), now)

    async def list_banners(self) -> list[BannerMessage]:
        result = await self.db.execute(select(BannerMessage).order_by(BannerMessage.priority.desc()))
        return list(result.scalars().all())

    async def create_banner(self, user_id: uuid.UUID, payload: BannerMessageCreate) -> BannerMessage:
        item = BannerMessage(**payload.model_dump())
        return await self.create_audited(item, user_id=user_id, entity_type="banner_message")

    async def update_banner(
        self,
        user_id: uuid.UUID,
        item_id: uuid.UUID,
        payload: BannerMessageUpdate,
    ) -> BannerMessage:
        item = await self.get_or_404(BannerMessage, item_id)
        updates = payload.model_dump(exclude_unset=True)
        return await self.update_audited(
            item,
            user_id=user_id,
            entity_type="banner_message",
            updates=updates,
        )

    async def delete_banner(self, user_id: uuid.UUID, item_id: uuid.UUID) -> None:
        item = await self.get_or_404(BannerMessage, item_id)
        await self.delete_audited(item, user_id=user_id, entity_type="banner_message")
