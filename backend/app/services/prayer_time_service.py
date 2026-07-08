import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import PrayerTime
from app.schemas import PrayerTimeCreate, PrayerTimeResponse, PrayerTimeUpdate
from app.services.base import BaseService
from app.services.days_utils import first_day_of_week
from app.services.prayer_time_resolver import enrich_prayer_time


class PrayerTimeService(BaseService):
    @staticmethod
    def _sort_by_first_day(items: list[PrayerTime]) -> list[PrayerTime]:
        return sorted(items, key=lambda item: first_day_of_week(item.days_of_week or []))

    @staticmethod
    def _validate_merged_prayer_time(item: PrayerTime) -> None:
        mode = item.time_mode or "fixed"
        if mode == "fixed":
            if not item.prayer_time:
                raise HTTPException(status_code=422, detail="שעה קבועה נדרשת במצב fixed")
            item.zman_ref = None
            item.offset_minutes = 0
        elif mode == "zmanim":
            if not item.zman_ref:
                raise HTTPException(status_code=422, detail="יש לבחור זמן הלכתי במצב zmanim")
            item.prayer_time = None

    async def to_prayer_time_response(self, item: PrayerTime) -> PrayerTimeResponse:
        return await enrich_prayer_time(item)

    async def to_prayer_time_responses(self, items: list[PrayerTime]) -> list[PrayerTimeResponse]:
        return [await self.to_prayer_time_response(item) for item in items]

    async def list_prayer_times(self) -> list[PrayerTimeResponse]:
        result = await self.db.execute(select(PrayerTime).order_by(PrayerTime.sort_order))
        items = self._sort_by_first_day(list(result.scalars().all()))
        return await self.to_prayer_time_responses(items)

    async def create_prayer_time(self, user_id: uuid.UUID, payload: PrayerTimeCreate) -> PrayerTimeResponse:
        item = PrayerTime(**payload.model_dump())
        await self.create_audited(
            item,
            user_id=user_id,
            entity_type="prayer_time",
            changes=payload.model_dump(),
        )
        return await self.to_prayer_time_response(item)

    async def update_prayer_time(
        self,
        user_id: uuid.UUID,
        item_id: uuid.UUID,
        payload: PrayerTimeUpdate,
    ) -> PrayerTimeResponse:
        item = await self.get_or_404(PrayerTime, item_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        self._validate_merged_prayer_time(item)
        await self.commit_audited_update(item, user_id=user_id, entity_type="prayer_time")
        return await self.to_prayer_time_response(item)

    async def delete_prayer_time(self, user_id: uuid.UUID, item_id: uuid.UUID) -> None:
        item = await self.get_or_404(PrayerTime, item_id)
        await self.delete_audited(item, user_id=user_id, entity_type="prayer_time")


async def resolve_prayer_time_responses(
    db: AsyncSession,
    items: list[PrayerTime],
) -> list[PrayerTimeResponse]:
    return await PrayerTimeService(db).to_prayer_time_responses(items)
