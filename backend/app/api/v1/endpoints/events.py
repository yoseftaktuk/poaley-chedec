import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.audit import log_audit
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Event, User
from app.schemas import EventCreate, EventResponse, EventUpdate
from app.services.image_cleanup import safe_delete_image
from app.services.utils import get_by_id, is_event_expired

router = APIRouter()


@router.get("", response_model=list[EventResponse])
async def list_events(
    homepage: bool = Query(default=False),
    db: AsyncSession = Depends(get_db),
) -> list[Event]:
    result = await db.execute(select(Event).order_by(Event.event_date))
    events = [e for e in result.scalars().all() if not is_event_expired(e)]
    if homepage:
        events = [e for e in events if e.show_on_homepage]
    return events


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    payload: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> Event:
    data = payload.model_dump()
    item = Event(**data)
    db.add(item)
    await log_audit(db, user_id=current_user.id, action="create", entity_type="event")
    await db.commit()
    await db.refresh(item)
    return item


@router.put("/{item_id}", response_model=EventResponse)
async def update_event(
    item_id: uuid.UUID,
    payload: EventUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> Event:
    item = await get_by_id(db, Event, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="לא נמצא")

    updates = payload.model_dump(exclude_unset=True)
    if updates.get("image_url") and updates.get("image_public_id") is None:
        updates.pop("image_public_id", None)

    old_public_id = item.image_public_id
    new_public_id = updates.get("image_public_id", item.image_public_id)
    new_image_url = updates.get("image_url", item.image_url)

    if "image_url" in updates and not new_image_url:
        updates["image_public_id"] = None

    for key, value in updates.items():
        setattr(item, key, value)

    if old_public_id and old_public_id != new_public_id:
        safe_delete_image(old_public_id)
    if "image_url" in updates and not new_image_url and old_public_id:
        safe_delete_image(old_public_id)

    await log_audit(db, user_id=current_user.id, action="update", entity_type="event", entity_id=item.id)
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    item_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> None:
    item = await get_by_id(db, Event, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="לא נמצא")
    safe_delete_image(item.image_public_id)
    await log_audit(db, user_id=current_user.id, action="delete", entity_type="event", entity_id=item.id)
    await db.delete(item)
    await db.commit()
