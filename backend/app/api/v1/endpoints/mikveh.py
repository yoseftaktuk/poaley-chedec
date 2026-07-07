from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.audit import log_audit
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Mikveh, User
from app.schemas import MikvehResponse, MikvehUpdate
from app.services.image_cleanup import safe_delete_image

router = APIRouter()


@router.get("", response_model=MikvehResponse)
async def get_mikveh(db: AsyncSession = Depends(get_db)) -> Mikveh:
    result = await db.execute(select(Mikveh).limit(1))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="תוכן מקווה לא נמצא")
    return item


@router.put("", response_model=MikvehResponse)
async def update_mikveh(
    payload: MikvehUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> Mikveh:
    result = await db.execute(select(Mikveh).limit(1))
    item = result.scalar_one_or_none()
    data = payload.model_dump()
    old_public_id = item.image_public_id if item else None

    if not item:
        item = Mikveh(**data)
        db.add(item)
    else:
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
        if old_public_id and old_public_id != new_public_id:
            safe_delete_image(old_public_id)
        if "image_url" in data and not new_image_url and old_public_id:
            safe_delete_image(old_public_id)

    await log_audit(db, user_id=current_user.id, action="update", entity_type="mikveh", entity_id=item.id)
    await db.commit()
    await db.refresh(item)
    return item
