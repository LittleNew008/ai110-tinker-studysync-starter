"""
Tinker 1B, Part 1: write an assert-based pytest test for session_rating()
BEFORE you touch anything else. One test is started for you -- add at least
one more.
"""

from scoring import session_rating


def test_session_rating_boundary_90_is_great():
    assert session_rating(90) == "Great"

def test_session_rating_boundary_59_is_skip():
    assert session_rating(59) == "Skip"

def test_session_rating_boundary_80_is_good():
    assert session_rating(80) == "Good"

# TODO: add at least one more test, e.g. a boundary case for "Skip" (a score
# of 59) or the exact boundary for "Good" (a score of 80).

# test negative score
def test_session_rating_negative_score():
    try:
        session_rating(-10)
    except ValueError as e:
        assert str(e) == "Expected non-negative score, got -10"
    else:
        assert False, "Expected ValueError for negative score"

# test score over 100
def test_session_rating_score_over_100():
    try:
        session_rating(150)
    except ValueError as e:
        assert str(e) == "Expected score <= 100, got 150"
    else:
        assert False, "Expected ValueError for score over 100"

# test decimal score
def test_session_rating_decimal_score():
    try:
        session_rating(85.5)
    except TypeError as e:
        assert str(e) == "Expected int, got float"
    else:
        assert False, "Expected TypeError for decimal score"

