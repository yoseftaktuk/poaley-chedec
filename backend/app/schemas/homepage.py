from pydantic import BaseModel

from app.schemas.banners import BannerMessageResponse
from app.schemas.events import EventResponse
from app.schemas.prayer_times import PrayerTimeResponse
from app.schemas.settings import HomepageSettingsSnapshot
from app.schemas.torah_lessons import TorahLessonResponse


class HomepageResponse(BaseModel):
    settings: HomepageSettingsSnapshot
    prayer_times: list[PrayerTimeResponse]
    torah_lessons: list[TorahLessonResponse]
    events: list[EventResponse]
    banners: list[BannerMessageResponse]
