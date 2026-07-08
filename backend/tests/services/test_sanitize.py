from datetime import date, datetime, time

from app.core.sanitize import sanitize_html, sanitize_text
from app.models import Event
from app.services.utils import combine_event_datetime, is_event_expired


def test_sanitize_text_strips_html():
    assert sanitize_text("<script>alert(1)</script>hello") == "hello"


def test_sanitize_html_allows_safe_tags():
    result = sanitize_html("<p>Hello <strong>world</strong></p>")
    assert "<p>" in result
    assert "<strong>" in result


def test_combine_event_datetime():
    result = combine_event_datetime(date(2026, 1, 15), "14:30")
    assert result == datetime(2026, 1, 15, 14, 30)


def test_is_event_expired_past_event():
    event = Event(
        title="Past",
        event_date=date(2020, 1, 1),
        event_time="10:00",
    )
    assert is_event_expired(event)


def test_is_event_expired_future_event():
    event = Event(
        title="Future",
        event_date=date(2099, 12, 31),
        event_time="23:59",
    )
    assert not is_event_expired(event)
