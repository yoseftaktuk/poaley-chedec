from zoneinfo import ZoneInfo

ISRAEL_TZ = ZoneInfo("Asia/Jerusalem")


def get_israel_weekday() -> int:
    """Return 0=Sunday (ראשון) through 6=Saturday (שבת)."""
    from datetime import datetime

    return (datetime.now(ISRAEL_TZ).weekday() + 1) % 7


def is_active_on_weekday(days_of_week: list[int] | None, weekday: int | None = None) -> bool:
    """Empty list means active every day (banners). Non-empty must include weekday."""
    if not days_of_week:
        return True
    day = weekday if weekday is not None else get_israel_weekday()
    return day in days_of_week


def normalize_days_of_week(days: list[int], *, allow_empty: bool = False) -> list[int]:
    unique = sorted(set(days))
    if not allow_empty and not unique:
        raise ValueError("At least one day must be selected")
    for day in unique:
        if day < 0 or day > 6:
            raise ValueError("Day must be between 0 and 6")
    return unique


def first_day_of_week(days_of_week: list[int]) -> int:
    return min(days_of_week) if days_of_week else 0
