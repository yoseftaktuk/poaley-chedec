from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    banners,
    contact,
    events,
    gallery,
    health,
    homepage,
    mikveh,
    prayer_times,
    seo,
    settings,
    torah_lessons,
    uploads,
)
from app.api.v1.endpoints.admin import router as admin_router

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(homepage.router, tags=["homepage"])
api_router.include_router(prayer_times.router, prefix="/prayer-times", tags=["prayer-times"])
api_router.include_router(torah_lessons.router, prefix="/torah-lessons", tags=["torah-lessons"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(gallery.router, prefix="/gallery", tags=["gallery"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
api_router.include_router(mikveh.router, prefix="/mikveh", tags=["mikveh"])
api_router.include_router(contact.router, prefix="/contact", tags=["contact"])
api_router.include_router(banners.router, prefix="/banners", tags=["banners"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(seo.router, tags=["seo"])
api_router.include_router(admin_router, prefix="/admin")
