from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.admin_service import AdminService
from app.services.banner_service import BannerService
from app.services.event_service import EventService
from app.services.gallery_service import GalleryService
from app.services.mikveh_service import MikvehService
from app.services.prayer_time_service import PrayerTimeService
from app.services.setting_service import SettingService
from app.services.torah_lesson_service import TorahLessonService


async def get_gallery_service(db: AsyncSession = Depends(get_db)) -> GalleryService:
    return GalleryService(db)


async def get_event_service(db: AsyncSession = Depends(get_db)) -> EventService:
    return EventService(db)


async def get_banner_service(db: AsyncSession = Depends(get_db)) -> BannerService:
    return BannerService(db)


async def get_prayer_time_service(db: AsyncSession = Depends(get_db)) -> PrayerTimeService:
    return PrayerTimeService(db)


async def get_torah_lesson_service(db: AsyncSession = Depends(get_db)) -> TorahLessonService:
    return TorahLessonService(db)


async def get_mikveh_service(db: AsyncSession = Depends(get_db)) -> MikvehService:
    return MikvehService(db)


async def get_setting_service(db: AsyncSession = Depends(get_db)) -> SettingService:
    return SettingService(db)


async def get_admin_service(db: AsyncSession = Depends(get_db)) -> AdminService:
    return AdminService(db)
