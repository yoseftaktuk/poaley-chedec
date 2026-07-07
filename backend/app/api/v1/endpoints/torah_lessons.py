import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.audit import log_audit
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import TorahLesson, User
from app.schemas import TorahLessonCreate, TorahLessonResponse, TorahLessonUpdate
from app.services.days_utils import first_day_of_week
from app.services.utils import get_by_id

router = APIRouter()


def _sort_by_first_day(items: list[TorahLesson]) -> list[TorahLesson]:
    return sorted(items, key=lambda item: first_day_of_week(item.days_of_week or []))


@router.get("", response_model=list[TorahLessonResponse])
async def list_torah_lessons(db: AsyncSession = Depends(get_db)) -> list[TorahLesson]:
    result = await db.execute(select(TorahLesson).where(TorahLesson.is_active.is_(True)))
    return _sort_by_first_day(list(result.scalars().all()))


@router.post("", response_model=TorahLessonResponse, status_code=status.HTTP_201_CREATED)
async def create_torah_lesson(
    payload: TorahLessonCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> TorahLesson:
    item = TorahLesson(**payload.model_dump())
    db.add(item)
    await log_audit(db, user_id=current_user.id, action="create", entity_type="torah_lesson")
    await db.commit()
    await db.refresh(item)
    return item


@router.put("/{item_id}", response_model=TorahLessonResponse)
async def update_torah_lesson(
    item_id: uuid.UUID,
    payload: TorahLessonUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> TorahLesson:
    item = await get_by_id(db, TorahLesson, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="לא נמצא")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    await log_audit(db, user_id=current_user.id, action="update", entity_type="torah_lesson", entity_id=item.id)
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_torah_lesson(
    item_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> None:
    item = await get_by_id(db, TorahLesson, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="לא נמצא")
    await log_audit(db, user_id=current_user.id, action="delete", entity_type="torah_lesson", entity_id=item.id)
    await db.delete(item)
    await db.commit()
