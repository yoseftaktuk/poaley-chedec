from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models import User
from app.schemas import PublicSettingsResponse, SettingResponse, SettingUpdate
from app.services.dependencies import get_setting_service
from app.services.setting_service import SettingService

router = APIRouter()


@router.get("/public", response_model=PublicSettingsResponse)
async def get_public_settings(
    service: SettingService = Depends(get_setting_service),
) -> PublicSettingsResponse:
    return await service.get_public_settings()


@router.get("/{section}", response_model=SettingResponse)
async def get_setting_section(
    section: str,
    current_user: Annotated[User, Depends(get_current_user)],
    service: SettingService = Depends(get_setting_service),
) -> SettingResponse:
    return await service.get_section(section)


@router.put("/{section}", response_model=SettingResponse)
async def update_setting_section(
    section: str,
    payload: SettingUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: SettingService = Depends(get_setting_service),
) -> SettingResponse:
    return await service.update_section(section, payload, current_user.id)
