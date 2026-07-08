import uuid

from sqlalchemy import select

from app.models import Event
from app.schemas import EventCreate, EventUpdate
from app.services.base import BaseService
from app.services.image_assets import cleanup_replaced_image, prepare_image_field_updates
from app.services.image_cleanup import safe_delete_image
from app.services.utils import is_event_expired


class EventService(BaseService):
    async def list_events(self, *, homepage_only: bool) -> list[Event]:
        result = await self.db.execute(select(Event).order_by(Event.event_date))
        events = [e for e in result.scalars().all() if not is_event_expired(e)]
        if homepage_only:
            events = [e for e in events if e.show_on_homepage]
        return events

    async def create_event(self, user_id: uuid.UUID, payload: EventCreate) -> Event:
        item = Event(**payload.model_dump())
        return await self.create_audited(item, user_id=user_id, entity_type="event")

    async def update_event(self, user_id: uuid.UUID, item_id: uuid.UUID, payload: EventUpdate) -> Event:
        item = await self.get_or_404(Event, item_id)
        updates = payload.model_dump(exclude_unset=True)
        updates, old_public_id, new_public_id, new_image_url = prepare_image_field_updates(
            item,
            updates,
            url_field="image_url",
            public_id_field="image_public_id",
        )
        for key, value in updates.items():
            setattr(item, key, value)
        cleanup_replaced_image(
            old_public_id,
            new_public_id,
            updates,
            url_field="image_url",
            new_url=new_image_url,
        )
        return await self.commit_audited_update(item, user_id=user_id, entity_type="event")

    async def delete_event(self, user_id: uuid.UUID, item_id: uuid.UUID) -> None:
        item = await self.get_or_404(Event, item_id)
        safe_delete_image(item.image_public_id)
        await self.delete_audited(item, user_id=user_id, entity_type="event")
