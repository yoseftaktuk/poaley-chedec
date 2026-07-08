import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.security import get_current_user
from app.models import TorahLesson, User
from app.schemas import TorahLessonCreate, TorahLessonResponse, TorahLessonUpdate
from app.services.dependencies import get_torah_lesson_service
from app.services.torah_lesson_service import TorahLessonService

router = APIRouter()


@router.get("", response_model=list[TorahLessonResponse])
async def list_torah_lessons(
    service: TorahLessonService = Depends(get_torah_lesson_service),
) -> list[TorahLesson]:
    return await service.list_active_lessons()


@router.post("", response_model=TorahLessonResponse, status_code=status.HTTP_201_CREATED)
async def create_torah_lesson(
    payload: TorahLessonCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: TorahLessonService = Depends(get_torah_lesson_service),
) -> TorahLesson:
    return await service.create_torah_lesson(current_user.id, payload)


@router.put("/{item_id}", response_model=TorahLessonResponse)
async def update_torah_lesson(
    item_id: uuid.UUID,
    payload: TorahLessonUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: TorahLessonService = Depends(get_torah_lesson_service),
) -> TorahLesson:
    return await service.update_torah_lesson(current_user.id, item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_torah_lesson(
    item_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    service: TorahLessonService = Depends(get_torah_lesson_service),
) -> None:
    await service.delete_torah_lesson(current_user.id, item_id)
