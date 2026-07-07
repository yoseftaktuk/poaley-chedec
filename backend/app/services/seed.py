import json
import logging
from email.message import EmailMessage

import aiosmtplib
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import hash_password
from app.models import (
    BannerMessage,
    Event,
    GalleryAlbum,
    Mikveh,
    PrayerTime,
    Setting,
    TorahLesson,
    User,
)

logger = logging.getLogger(__name__)

DEFAULT_SETTINGS: dict[str, dict] = {
    "homepage": {
        "welcome_title": "ברוכים הבאים לבית כנסת פועלי צדק",
        "welcome_text": "בית כנסת ומקווה באשקלון",
        "rabbi_message": "שלום וברכה לכל בני הקהילה",
        "rabbi_name": "אליהו תקתוק",
    },
    "contact": {
        "rabbi_name": "אליהו תקתוק",
        "address": "אפרים 52, אשקלון",
        "phone": "0544329218",
        "whatsapp": "0544329218",
        "email": "taktuk01@gmail.com",
        "maps_url": "https://maps.google.com/?q=אפרים+52+אשקלון",
    },
    "donation": {
        "bit_url": "https://meshulam.co.il/s/fc6cca97-e89b-5cbc-bda4-74b2fed13e92",
        "button_text": "תרומה לבית הכנסת",
    },
    "site": {
        "site_name": "בית כנסת פועלי צדק",
        "site_description": "בית כנסת ומקווה באשקלון",
    },
    "seo_global": {
        "title": "בית כנסת פועלי צדק | אשקלון",
        "description": "בית כנסת פועלי צדק ומקווה באשקלון - זמני תפילות, שיעורי תורה, אירועים ועוד",
        "og_image": "",
    },
    "seo_pages": {
        "home": {"title": "דף הבית", "description": "ברוכים הבאים לבית כנסת פועלי צדק"},
        "gallery": {"title": "גלריה", "description": "גלריית תמונות"},
        "mikveh": {"title": "מקווה", "description": "מידע על המקווה"},
        "contact": {"title": "צור קשר", "description": "יצירת קשר עם בית הכנסת"},
    },
    "accessibility_statement": {
        "title": "הצהרת נגישות",
        "content": "אתר זה מונגש בהתאם לתקנות נגישות.",
    },
}


async def seed_admin_users(db: AsyncSession) -> None:
    result = await db.execute(select(User))
    if result.scalars().first():
        return

    try:
        users_data = json.loads(settings.admin_users)
    except json.JSONDecodeError:
        logger.error("Invalid ADMIN_USERS JSON")
        return

    for user_data in users_data:
        username = user_data.get("username")
        password = user_data.get("password")
        if not username or not password:
            continue
        db.add(User(username=username, password_hash=hash_password(password)))
    await db.commit()


async def seed_default_settings(db: AsyncSession) -> None:
    for key, value in DEFAULT_SETTINGS.items():
        result = await db.execute(select(Setting).where(Setting.key == key))
        if result.scalar_one_or_none() is None:
            db.add(Setting(key=key, value=value))
    await db.commit()


async def seed_mikveh(db: AsyncSession) -> None:
    result = await db.execute(select(Mikveh))
    if result.scalars().first():
        return
    db.add(
        Mikveh(
            general_info="מקווה בית כנסת פועלי צדק - מקום טהרה וקדושה לקהילה.",
            regulations="יש לשמור על ניקיון וסדר במקווה.",
            avrech_price=10.0,
            regular_price=15.0,
            opening_schedules=[
                {
                    "days_of_week": [0, 1, 2, 3, 4],
                    "hours": "בזמן תפילות לאורך השבוע",
                },
                {
                    "days_of_week": [5],
                    "hours": "מ-12:00 ועד כניסת השבת",
                },
            ],
        )
    )
    await db.commit()


async def seed_fix_contact_settings(db: AsyncSession) -> None:
    result = await db.execute(select(Setting).where(Setting.key == "contact"))
    setting = result.scalar_one_or_none()
    if not setting:
        return
    defaults = DEFAULT_SETTINGS["contact"]
    address = setting.value.get("address", "")
    email = setting.value.get("email", "")
    if address in ("פרים 52, אשקלון", "אפרים צור 52, אשקלון") or email == "taktuk07@gmail.com":
        setting.value = {**setting.value, **defaults}
        await db.commit()


async def seed_fix_donation_settings(db: AsyncSession) -> None:
    result = await db.execute(select(Setting).where(Setting.key == "donation"))
    setting = result.scalar_one_or_none()
    if not setting:
        return
    defaults = DEFAULT_SETTINGS["donation"]
    bit_url = setting.value.get("bit_url", "")
    if bit_url in ("https://bit.ly/", "https://bit.ly"):
        setting.value = {**setting.value, **defaults}
        await db.commit()


async def run_seed(db: AsyncSession) -> None:
    await seed_admin_users(db)
    await seed_default_settings(db)
    await seed_fix_contact_settings(db)
    await seed_fix_donation_settings(db)
    await seed_mikveh(db)


async def get_setting(db: AsyncSession, key: str) -> dict:
    result = await db.execute(select(Setting).where(Setting.key == key))
    setting = result.scalar_one_or_none()
    return setting.value if setting else DEFAULT_SETTINGS.get(key, {})


async def upsert_setting(db: AsyncSession, key: str, value: dict) -> Setting:
    result = await db.execute(select(Setting).where(Setting.key == key))
    setting = result.scalar_one_or_none()
    if setting:
        setting.value = value
    else:
        setting = Setting(key=key, value=value)
        db.add(setting)
    await db.commit()
    await db.refresh(setting)
    return setting


async def send_contact_email(name: str, phone: str, email: str, message: str) -> bool:
    if not settings.smtp_host or not settings.smtp_user:
        logger.warning("SMTP not configured, skipping email send")
        return False

    msg = EmailMessage()
    msg["From"] = settings.smtp_from
    msg["To"] = settings.contact_recipient_email
    msg["Subject"] = f"הודעה חדשה מאתר בית כנסת פועלי צדק - {name}"
    msg.set_content(
        f"שם: {name}\nטלפון: {phone}\nאימייל: {email}\n\nהודעה:\n{message}",
        charset="utf-8",
    )

    try:
        await aiosmtplib.send(
            msg,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_user,
            password=settings.smtp_password,
            start_tls=True,
        )
        return True
    except Exception:
        logger.exception("Failed to send contact email")
        return False
