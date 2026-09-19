# tests/test_rehearsals.py
from rehearsals import (
    calculate_rehearsal_cost,
    check_room_suitability,
    is_band_available,
    add_rehearsal,
    cancel_rehearsal,
)


def test_calculate_rehearsal_cost():
    result = calculate_rehearsal_cost(2000.0, 4, False)
    assert result == 500.0


def test_calculate_rehearsal_cost_with_discount():
    result = calculate_rehearsal_cost(2000.0, 4, True)
    assert result == 400.0


def test_check_room_suitability():
    result = check_room_suitability(5, 4, False)
    assert result == "Помещение отлично подходит!"


def test_is_band_available():
    rehearsals = []
    assert is_band_available(rehearsals, 1, "2026-09-15") is True


def test_duplicate_rehearsal_forbidden():
    rehearsals = []
    add_rehearsal(rehearsals, 1, "2026-09-15", 4)
    assert is_band_available(rehearsals, 1, "2026-09-15") is False


def test_cancel_rehearsal():
    rehearsals = []
    add_rehearsal(rehearsals, 1, "2026-09-15", 4)
    assert cancel_rehearsal(rehearsals, 1) is True
    assert len(rehearsals) == 0
