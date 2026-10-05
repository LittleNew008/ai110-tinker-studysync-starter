from datetime import date

import pytest

from sessions import find_conflicts, next_occurrence


# --- find_conflicts ---

def test_empty_list_returns_empty_list():
    assert find_conflicts([]) == []


def test_single_session_returns_empty_list():
    assert find_conflicts([{"subject": "Calc II", "slot": "08:00"}]) == []


def test_no_shared_slots_returns_empty_list():
    sessions = [{"slot": "08:00"}, {"slot": "09:00"}]
    assert find_conflicts(sessions) == []


def test_one_conflicting_pair():
    a = {"subject": "Calc II", "slot": "08:00"}
    b = {"subject": "Chem Lab", "slot": "08:00"}
    c = {"subject": "History", "slot": "09:00"}
    assert find_conflicts([a, b, c]) == [(a, b)]


def test_three_in_one_slot_gives_every_pair():
    a, b, c = ({"subject": s, "slot": "08:00"} for s in "abc")
    assert find_conflicts([a, b, c]) == [(a, b), (a, c), (b, c)]


def test_two_separate_conflicting_slots():
    a1, a2 = {"subject": "a1", "slot": "08:00"}, {"subject": "a2", "slot": "08:00"}
    b1, b2 = {"subject": "b1", "slot": "09:00"}, {"subject": "b2", "slot": "09:00"}
    assert find_conflicts([a1, b1, a2, b2]) == [(a1, a2), (b1, b2)]


def test_no_session_is_paired_with_itself():
    sessions = [{"slot": "08:00"}, {"slot": "08:00"}]
    for first, second in find_conflicts(sessions):
        assert first is not second


# --- next_occurrence ---

def test_daily_adds_one_day():
    assert next_occurrence(date(2026, 1, 1), "daily") == date(2026, 1, 2)


def test_weekly_adds_seven_days():
    assert next_occurrence(date(2026, 1, 1), "weekly") == date(2026, 1, 8)


def test_daily_rolls_over_month_end():
    assert next_occurrence(date(2026, 1, 31), "daily") == date(2026, 2, 1)


def test_weekly_rolls_over_year_end():
    assert next_occurrence(date(2026, 12, 28), "weekly") == date(2027, 1, 4)


def test_daily_handles_leap_day():
    assert next_occurrence(date(2028, 2, 28), "daily") == date(2028, 2, 29)


def test_unknown_frequency_raises_key_error():
    with pytest.raises(KeyError):
        next_occurrence(date(2026, 1, 1), "monthly")
