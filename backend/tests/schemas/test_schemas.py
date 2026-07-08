import uuid

import pytest
from pydantic import ValidationError

from app.schemas import (
    ContactCreate,
    LoginRequest,
    MessageResponse,
    PrayerTimeCreate,
    PrayerTimeUpdate,
    PublicSettingsResponse,
)


def test_login_request_valid():
    req = LoginRequest(username="admin", password="secret")
    assert req.username == "admin"


def test_contact_create_valid():
    contact = ContactCreate(
        name="ישראל ישראלי",
        phone="0501234567",
        email="test@example.com",
        message="שלום, הודעה לבדיקה",
    )
    assert contact.name == "ישראל ישראלי"


def test_contact_create_invalid_email():
    with pytest.raises(ValidationError):
        ContactCreate(
            name="Test",
            phone="0501234567",
            email="not-an-email",
            message="Hello world test",
        )


def test_contact_create_short_name():
    with pytest.raises(ValidationError):
        ContactCreate(
            name="A",
            phone="0501234567",
            email="test@example.com",
            message="Hello world test",
        )


def test_prayer_time_create_valid_days():
    pt = PrayerTimeCreate(
        prayer_name="שחרית",
        days_of_week=[0, 1, 2],
        prayer_time="06:30",
    )
    assert pt.days_of_week == [0, 1, 2]


def test_prayer_time_create_invalid_day():
    with pytest.raises(ValidationError):
        PrayerTimeCreate(
            prayer_name="שחרית",
            days_of_week=[8],
            prayer_time="06:30",
        )


def test_prayer_time_create_empty_days():
    with pytest.raises(ValidationError):
        PrayerTimeCreate(
            prayer_name="שחרית",
            days_of_week=[],
            prayer_time="06:30",
        )


def test_prayer_time_create_zmanim_requires_ref():
    with pytest.raises(ValidationError):
        PrayerTimeCreate(
            prayer_name="מעריב",
            days_of_week=[0, 1, 2, 3, 4, 5, 6],
            time_mode="zmanim",
            offset_minutes=20,
        )


def test_prayer_time_create_zmanim_valid():
    pt = PrayerTimeCreate(
        prayer_name="מעריב",
        days_of_week=[0, 1, 2, 3, 4, 5, 6],
        time_mode="zmanim",
        zman_ref="sunset",
        offset_minutes=20,
    )
    assert pt.zman_ref.value == "sunset"
    assert pt.prayer_time is None


def test_prayer_time_update_partial():
    update = PrayerTimeUpdate(prayer_name="מנחה")
    assert update.prayer_name == "מנחה"
    assert update.days_of_week is None


def test_message_response():
    response = MessageResponse(message="ההודעה נשלחה בהצלחה")
    assert response.message == "ההודעה נשלחה בהצלחה"


def test_public_settings_response():
    settings = PublicSettingsResponse(
        contact={"phone": "0501234567"},
        donation={"bit_url": "https://example.com"},
        site={"site_name": "בית כנסת"},
        seo_global={"title": "SEO"},
        seo_pages={"home": {"title": "דף הבית"}},
        accessibility_statement={"title": "נגישות"},
        homepage={"welcome_title": "ברוכים הבאים"},
    )
    assert settings.contact["phone"] == "0501234567"
    assert settings.seo_pages["home"]["title"] == "דף הבית"
