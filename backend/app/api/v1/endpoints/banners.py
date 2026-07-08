import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.security import get_current_user
from app.models import BannerMessage, User
from app.schemas import BannerMessageCreate, BannerMessageResponse, BannerMessageUpdate
from app.services.banner_service import BannerService
from app.services.dependencies import get_banner_service

router = APIRouter()


@router.get("/active", response_model=list[BannerMessageResponse])
async def list_active_banners(
    service: BannerService = Depends(get_banner_service),
) -> list[BannerMessage]:
    return await service.list_active_banners()


@router.get("", response_model=list[BannerMessageResponse])
async def list_banners(
    current_user: Annotated[User, Depends(get_current_user)],
    service: BannerService = Depends(get_banner_service),
) -> list[BannerMessage]:
    return await service.list_banners()


@router.post("", response_model=BannerMessageResponse, status_code=status.HTTP_201_CREATED)
async def create_banner(
    payload: BannerMessageCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: BannerService = Depends(get_banner_service),
) -> BannerMessage:
    return await service.create_banner(current_user.id, payload)


@router.put("/{item_id}", response_model=BannerMessageResponse)
async def update_banner(
    item_id: uuid.UUID,
    payload: BannerMessageUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: BannerService = Depends(get_banner_service),
) -> BannerMessage:
    return await service.update_banner(current_user.id, item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_banner(
    item_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    service: BannerService = Depends(get_banner_service),
) -> None:
    await service.delete_banner(current_user.id, item_id)
