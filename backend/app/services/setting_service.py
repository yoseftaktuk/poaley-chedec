import uuid

from fastapi import HTTPException

from app.core.audit import log_audit
from app.schemas import PublicSettingsResponse, SettingResponse, SettingUpdate
from app.services.base import BaseService
from app.services.seed import DEFAULT_SETTINGS, get_setting, upsert_setting

PUBLIC_KEYS = frozenset(
    {"contact", "donation", "site", "seo_global", "seo_pages", "accessibility_statement", "homepage"}
)


class SettingService(BaseService):
    async def get_public_settings(self) -> PublicSettingsResponse:
        data = {key: await get_setting(self.db, key) for key in PUBLIC_KEYS}
        return PublicSettingsResponse(**data)

    async def get_section(self, section: str) -> SettingResponse:
        if section not in DEFAULT_SETTINGS:
            raise HTTPException(status_code=404, detail="הגדרה לא נמצאה")
        value = await get_setting(self.db, section)
        return SettingResponse(key=section, value=value)

    async def update_section(
        self,
        section: str,
        payload: SettingUpdate,
        user_id: uuid.UUID,
    ) -> SettingResponse:
        if section not in DEFAULT_SETTINGS:
            raise HTTPException(status_code=404, detail="הגדרה לא נמצאה")
        setting = await upsert_setting(self.db, section, payload.value)
        await log_audit(
            self.db,
            user_id=user_id,
            action="update",
            entity_type="setting",
            changes={"key": section},
        )
        await self.db.commit()
        return SettingResponse(key=setting.key, value=setting.value)
