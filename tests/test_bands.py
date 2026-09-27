# tests/test_bands.py
from models import Band
from models.band import (
    add_band,
    check_band_capacity,
    filter_bands_by_active,
    find_band,
    get_band_status,
    get_bands_stats,
    iter_active_bands,
    sort_bands,
)
from models.member import evaluate_candidate
from models.rehearsal import Rehearsal


def test_band_creation():
    band = Band(1, "Nirvana", "2026-06-06", "Бас-гитара", True)
    assert band.id == 1
    assert band.name == "Nirvana"
    assert band.required_instrument == "Бас-гитара"
    assert band.is_active is True
    assert band.members == []


def test_band_str():
    band = Band(1, "Nirvana", "2026-06-06", "Бас-гитара", True)
    text = str(band)
    assert "Nirvana" in text
    assert "Бас-гитара" in text


def test_band_is_suitable_for():
    band = Band(1, "A", "2026-01-01", "Гитара", True,
                members=["A", "B", "C"])
    assert band.is_suitable_for(3) is True
    assert band.is_suitable_for(5) is False


def test_band_validate_capacity():
    assert Band.validate_capacity(3) is True
    assert Band.validate_capacity(0) is True


def test_band_from_data_to_dict():
    data = {
        "id": 1,
        "name": "Nirvana",
        "foundation_date": "2026-06-06",
        "required_instrument": "Бас-гитара",
        "is_active": True,
        "members": ["A"],
    }
    band = Band.from_data(data)
    assert band.name == "Nirvana"
    assert band.to_dict() == data


def test_add_band():
    bands = []
    band = add_band(bands, "Nirvana", "2026-06-06", "Бас-гитара", True)
    assert len(bands) == 1
    assert isinstance(band, Band)
    assert band.id == 1


def test_find_band():
    bands = []
    add_band(bands, "Nirvana", "2026-06-06", "Бас-гитара", True)
    results = find_band(bands, "irvana")
    assert len(results) == 1
    assert results[0].name == "Nirvana"


def test_check_band_capacity():
    bands = []
    add_band(bands, "Nirvana", "2026-06-06", "Бас-гитара", True)
    assert check_band_capacity(bands, 1, 0) is True


def test_check_band_capacity_with_members():
    bands = []
    band = add_band(bands, "Nirvana", "2026-06-06", "Бас-гитара", True)
    band.members = ["A", "B", "C"]
    assert check_band_capacity(bands, 1, 3) is True
    assert check_band_capacity(bands, 1, 5) is False
    assert check_band_capacity(bands, 999, 0) is False


def test_sort_bands():
    bands = []
    add_band(bands, "Zebra", "2026-01-01", "Гитара", True)
    add_band(bands, "Alpha", "2026-02-01", "Бас", True)
    ordered = sort_bands(bands)
    assert ordered[0].name == "Alpha"


def test_evaluate_candidate():
    result = evaluate_candidate("Бас-гитара", "Бас-гитара", 3)
    assert result == "Одобрено: Приглашаем на прослушивание!"


def test_evaluate_candidate_wrong_instrument():
    result = evaluate_candidate("Скрипка", "Бас-гитара", 5)
    assert result == "Отказ: Нам нужен другой инструмент."


def test_filter_bands_by_active():
    bands = []
    add_band(bands, "A", "2026-01-01", "Гитара", True)
    add_band(bands, "B", "2026-01-02", "Бас", False)
    assert len(filter_bands_by_active(bands, True)) == 1
    assert len(filter_bands_by_active(bands, False)) == 1


def test_iter_active_bands():
    bands = []
    add_band(bands, "A", "2026-01-01", "Гитара", True)
    add_band(bands, "B", "2026-01-02", "Бас", False)
    result = list(iter_active_bands(bands))
    assert len(result) == 1
    assert result[0].name == "A"


def test_get_bands_stats():
    bands = []
    add_band(bands, "A", "2026-01-01", "Гитара", True)
    band_b = add_band(bands, "B", "2026-01-02", "Бас", False)
    band_a = bands[0]
    rehearsals = [
        Rehearsal(1, band_a, "2026-09-15", 4),
        Rehearsal(2, band_b, "2026-09-16", 2),
    ]
    stats = get_bands_stats(bands, rehearsals)
    assert stats["total_bands"] == 2
    assert stats["active_bands"] == 1
    assert stats["total_rehearsals"] == 2
    assert stats["avg_participants"] == 3.0


def test_get_bands_stats_empty():
    stats = get_bands_stats([], [])
    assert stats["total_bands"] == 0
    assert stats["avg_participants"] == 0.0


def test_get_band_status():
    assert get_band_status(True) == "Группа доступна для прослушивания"
    assert get_band_status(False) == "Группа уже занята"
