from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.audit import log_audit
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User
from app.schemas import SettingResponse, SettingUpdate
from app.services.seed import DEFAULT_SETTINGS, get_setting, upsert_setting

router = APIRouter()

PUBLIC_KEYS = {"contact", "donation", "site", "seo_global", "seo_pages", "accessibility_statement", "homepage"}


@router.get("/public")
async def get_public_settings(db: AsyncSession = Depends(get_db)) -> dict[str, dict]:
    result = {}
    for key in PUBLIC_KEYS:
        result[key] = await get_setting(db, key)
    return result


@router.get("/{section}", response_model=SettingResponse)
async def get_setting_section(
    section: str,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> SettingResponse:
    if section not in DEFAULT_SETTINGS:
        raise HTTPException(status_code=404, detail="הגדרה לא נמצאה")
    value = await get_setting(db, section)
    return SettingResponse(key=section, value=value)


@router.put("/{section}", response_model=SettingResponse)
async def update_setting_section(
    section: str,
    payload: SettingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> SettingResponse:
    if section not in DEFAULT_SETTINGS:
        raise HTTPException(status_code=404, detail="הגדרה לא נמצאה")
    setting = await upsert_setting(db, section, payload.value)
    await log_audit(
        db,
        user_id=current_user.id,
        action="update",
        entity_type="setting",
        changes={"key": section},
    )
    await db.commit()
    return SettingResponse(key=setting.key, value=setting.value)
