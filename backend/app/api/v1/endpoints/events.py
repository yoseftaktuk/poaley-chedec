import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.core.security import get_current_user
from app.models import Event, User
from app.schemas import EventCreate, EventResponse, EventUpdate
from app.services.dependencies import get_event_service
from app.services.event_service import EventService

router = APIRouter()


@router.get("", response_model=list[EventResponse])
async def list_events(
    homepage: bool = Query(default=False),
    service: EventService = Depends(get_event_service),
) -> list[Event]:
    return await service.list_events(homepage_only=homepage)


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    payload: EventCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: EventService = Depends(get_event_service),
) -> Event:
    return await service.create_event(current_user.id, payload)


@router.put("/{item_id}", response_model=EventResponse)
async def update_event(
    item_id: uuid.UUID,
    payload: EventUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: EventService = Depends(get_event_service),
) -> Event:
    return await service.update_event(current_user.id, item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    item_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    service: EventService = Depends(get_event_service),
) -> None:
    await service.delete_event(current_user.id, item_id)
