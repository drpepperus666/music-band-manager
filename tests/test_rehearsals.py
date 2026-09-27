# tests/test_rehearsals.py
from models import Band, Rehearsal
from models.band import add_band
from models.member import Member
from models.rehearsal import (
    add_rehearsal,
    calculate_rehearsal_cost,
    cancel_rehearsal,
    check_room_suitability,
    create_rehearsal,
    is_band_available,
)


def make_band(band_id=1):
    return Band(band_id, "Nirvana", "2026-06-06", "Бас-гитара", True)


def make_user(user_id=1, bands=None):
    band = (bands or [make_band()])[0]
    return Member(user_id, band, "Бас-гитара", 3)


def test_rehearsal_creation():
    band = make_band()
    rehearsal = Rehearsal(1, band, "2026-09-15", 4)
    assert rehearsal.id == 1
    assert rehearsal.band is band
    assert rehearsal.band_id == 1
    assert rehearsal.rehearsal_date == "2026-09-15"
    assert rehearsal.is_cancelled is False


def test_rehearsal_str_and_cancel():
    band = make_band()
    rehearsal = Rehearsal(1, band, "2026-09-15", 4)
    assert "Nirvana" in str(rehearsal)
    rehearsal.cancel()
    assert rehearsal.is_cancelled is True
    assert "отменена" in str(rehearsal)


def test_calculate_rehearsal_cost():
    assert calculate_rehearsal_cost(2000.0, 4, False) == 500.0


def test_calculate_rehearsal_cost_with_discount():
    assert calculate_rehearsal_cost(2000.0, 4, True) == 400.0


def test_check_room_suitability():
    assert check_room_suitability(5, 4, False) == "Помещение отлично подходит!"


def test_is_band_available():
    assert is_band_available([], 1, "2026-09-15") is True


def test_duplicate_rehearsal_forbidden():
    bands = []
    band = add_band(bands, "Nirvana", "2026-06-06", "Бас-гитара", True)
    rehearsals = []
    created = create_rehearsal(rehearsals, band, None, "2026-09-15", 4)
    assert created is not None
    assert is_band_available(rehearsals, band, "2026-09-15") is False
    second = create_rehearsal(rehearsals, band, None, "2026-09-15", 2)
    assert second is None
    assert len(rehearsals) == 1


def test_cancelled_does_not_block():
    bands = []
    band = add_band(bands, "Nirvana", "2026-06-06", "Бас-гитара", True)
    rehearsals = []
    first = create_rehearsal(rehearsals, band, None, "2026-09-15", 4)
    first.cancel()
    assert is_band_available(rehearsals, band, "2026-09-15") is True
    second = create_rehearsal(rehearsals, band, None, "2026-09-15", 2)
    assert second is not None


def test_cancel_rehearsal():
    bands = []
    band = add_band(bands, "Nirvana", "2026-06-06", "Бас-гитара", True)
    rehearsals = []
    add_rehearsal(rehearsals, band, "2026-09-15", 4)
    assert cancel_rehearsal(rehearsals, 1) is True
    assert len(rehearsals) == 1
    assert rehearsals[0].is_cancelled is True


def test_cancel_rehearsal_not_found():
    bands = []
    band = add_band(bands, "Nirvana", "2026-06-06", "Бас-гитара", True)
    rehearsals = []
    add_rehearsal(rehearsals, band, "2026-09-15", 4)
    assert cancel_rehearsal(rehearsals, 999) is False
    assert len(rehearsals) == 1


def test_rehearsal_from_data_to_dict():
    bands = [make_band(1)]
    data = {
        "id": 1,
        "band_id": 1,
        "rehearsal_date": "2026-09-15",
        "participants": 4,
        "is_cancelled": False,
    }
    rehearsal = Rehearsal.from_data(data, bands)
    assert rehearsal is not None
    assert rehearsal.band is bands[0]
    assert rehearsal.to_dict() == data
