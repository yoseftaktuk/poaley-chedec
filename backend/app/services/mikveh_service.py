import uuid

from fastapi import HTTPException
from sqlalchemy import select

from app.models import Mikveh
from app.schemas import MikvehUpdate
from app.services.base import BaseService
from app.services.image_assets import cleanup_replaced_image, prepare_image_field_updates


class MikvehService(BaseService):
    async def get_mikveh(self) -> Mikveh:
        result = await self.db.execute(select(Mikveh).limit(1))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="תוכן מקווה לא נמצא")
        return item

    async def upsert_mikveh(self, user_id: uuid.UUID, payload: MikvehUpdate) -> Mikveh:
        result = await self.db.execute(select(Mikveh).limit(1))
        item = result.scalar_one_or_none()
        data = payload.model_dump()
        old_public_id = item.image_public_id if item else None

        if not item:
            item = Mikveh(**data)
            return await self.create_audited(item, user_id=user_id, entity_type="mikveh", action="update")

        new_public_id = data.get("image_public_id", item.image_public_id)
        new_image_url = data.get("image_url", item.image_url)
        if data.get("image_url") and data.get("image_public_id") is None:
            data.pop("image_public_id", None)
        if "image_url" in data and not new_image_url:
            data["image_public_id"] = None
        for key, value in data.items():
            if key == "opening_schedules":
                value = [
                    schedule.model_dump() if hasattr(schedule, "model_dump") else schedule
                    for schedule in value
                ]
            setattr(item, key, value)
        cleanup_replaced_image(
            old_public_id,
            new_public_id,
            data,
            url_field="image_url",
            new_url=new_image_url,
        )
        return await self.commit_audited_update(item, user_id=user_id, entity_type="mikveh")
