from typing import Any

from pydantic import BaseModel


class SettingUpdate(BaseModel):
    value: dict[str, Any]


class SettingResponse(BaseModel):
    key: str
    value: dict[str, Any]


class HomepageSettingsSnapshot(BaseModel):
    homepage: dict[str, Any]
    contact: dict[str, Any]
    donation: dict[str, Any]
    site: dict[str, Any]


class PublicSettingsResponse(BaseModel):
    contact: dict[str, Any]
    donation: dict[str, Any]
    site: dict[str, Any]
    seo_global: dict[str, Any]
    seo_pages: dict[str, Any]
    accessibility_statement: dict[str, Any]
    homepage: dict[str, Any]
