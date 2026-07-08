import pytest

from app.services.days_utils import (
    first_day_of_week,
    is_active_on_weekday,
    normalize_days_of_week,
)


def test_normalize_days_of_week_sorts_and_dedupes():
    assert normalize_days_of_week([3, 1, 1, 2]) == [1, 2, 3]


def test_normalize_days_rejects_empty_when_not_allowed():
    with pytest.raises(ValueError, match="At least one day"):
        normalize_days_of_week([], allow_empty=False)


def test_normalize_days_allows_empty():
    assert normalize_days_of_week([], allow_empty=True) == []


def test_normalize_days_rejects_invalid_day():
    with pytest.raises(ValueError, match="between 0 and 6"):
        normalize_days_of_week([7])


def test_is_active_on_weekday_empty_means_always_active():
    assert is_active_on_weekday([], weekday=3)


def test_is_active_on_weekday_checks_membership():
    assert is_active_on_weekday([1, 3], weekday=1)
    assert not is_active_on_weekday([1, 3], weekday=2)


def test_first_day_of_week():
    assert first_day_of_week([3, 1, 5]) == 1
    assert first_day_of_week([]) == 0
