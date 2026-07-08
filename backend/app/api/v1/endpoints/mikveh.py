from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models import Mikveh, User
from app.schemas import MikvehResponse, MikvehUpdate
from app.services.dependencies import get_mikveh_service
from app.services.mikveh_service import MikvehService

router = APIRouter()


@router.get("", response_model=MikvehResponse)
async def get_mikveh(service: MikvehService = Depends(get_mikveh_service)) -> Mikveh:
    return await service.get_mikveh()


@router.put("", response_model=MikvehResponse)
async def update_mikveh(
    payload: MikvehUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: MikvehService = Depends(get_mikveh_service),
) -> Mikveh:
    return await service.upsert_mikveh(current_user.id, payload)
