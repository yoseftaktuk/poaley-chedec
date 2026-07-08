import uuid

from sqlalchemy import select

from app.models import TorahLesson
from app.schemas import TorahLessonCreate, TorahLessonUpdate
from app.services.base import BaseService
from app.services.days_utils import first_day_of_week


class TorahLessonService(BaseService):
    @staticmethod
    def _sort_by_first_day(items: list[TorahLesson]) -> list[TorahLesson]:
        return sorted(items, key=lambda item: first_day_of_week(item.days_of_week or []))

    async def list_active_lessons(self) -> list[TorahLesson]:
        result = await self.db.execute(select(TorahLesson).where(TorahLesson.is_active.is_(True)))
        return self._sort_by_first_day(list(result.scalars().all()))

    async def create_torah_lesson(self, user_id: uuid.UUID, payload: TorahLessonCreate) -> TorahLesson:
        item = TorahLesson(**payload.model_dump())
        return await self.create_audited(item, user_id=user_id, entity_type="torah_lesson")

    async def update_torah_lesson(
        self,
        user_id: uuid.UUID,
        item_id: uuid.UUID,
        payload: TorahLessonUpdate,
    ) -> TorahLesson:
        item = await self.get_or_404(TorahLesson, item_id)
        updates = payload.model_dump(exclude_unset=True)
        return await self.update_audited(
            item,
            user_id=user_id,
            entity_type="torah_lesson",
            updates=updates,
        )

    async def delete_torah_lesson(self, user_id: uuid.UUID, item_id: uuid.UUID) -> None:
        item = await self.get_or_404(TorahLesson, item_id)
        await self.delete_audited(item, user_id=user_id, entity_type="torah_lesson")
