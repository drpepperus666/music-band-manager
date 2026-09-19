# tests/test_bands.py
from bands import add_band, find_band, check_band_capacity, sort_bands, \
    evaluate_candidate


def test_add_band():
    bands = []
    add_band(bands, "Nirvana", "2026-06-06", "Бас-гитара", True)
    assert len(bands) == 1


def test_find_band():
    bands = []
    add_band(bands, "Nirvana", "2026-06-06", "Бас-гитара", True)
    results = find_band(bands, "irvana")
    assert len(results) == 1


def test_check_band_capacity():
    bands = []
    add_band(bands, "Nirvana", "2026-06-06", "Бас-гитара", True)
    assert check_band_capacity(bands, 1, 0) is True


def test_sort_bands():
    bands = []
    add_band(bands, "Zebra", "2026-01-01", "Гитара", True)
    add_band(bands, "Alpha", "2026-02-01", "Бас", True)
    sorted_bands = sort_bands(bands)
    assert sorted_bands[0]['name'] == 'Alpha'


def test_evaluate_candidate():
    result = evaluate_candidate("Бас-гитара", "Бас-гитара", 3)
    assert result == "Одобрено: Приглашаем на прослушивание!"


def test_evaluate_candidate_wrong_instrument():
    result = evaluate_candidate("Скрипка", "Бас-гитара", 5)
    assert result == "Отказ: Нам нужен другой инструмент."
