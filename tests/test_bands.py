# tests/test_bands.py
from bands import add_band, find_band, check_band_capacity, sort_bands, \
    evaluate_candidate, filter_bands_by_active, iter_active_bands, \
    get_bands_stats, get_band_status


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


def test_check_band_capacity_with_members():
    bands = []
    add_band(bands, "Nirvana", "2026-06-06", "Бас-гитара", True)
    bands[0]['members'] = ["A", "B", "C"]
    assert check_band_capacity(bands, 1, 3) is True
    assert check_band_capacity(bands, 1, 5) is False
    assert check_band_capacity(bands, 999, 0) is False


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
    assert result[0]['name'] == "A"


def test_get_bands_stats():
    bands = []
    add_band(bands, "A", "2026-01-01", "Гитара", True)
    add_band(bands, "B", "2026-01-02", "Бас", False)
    rehearsals = [
        {'id': 1, 'band_id': 1,
         'rehearsal_date': '2026-09-15', 'participants': 4},
        {'id': 2, 'band_id': 2,
         'rehearsal_date': '2026-09-16', 'participants': 2},
    ]
    stats = get_bands_stats(bands, rehearsals)
    assert stats['total_bands'] == 2
    assert stats['active_bands'] == 1
    assert stats['total_rehearsals'] == 2
    assert stats['avg_participants'] == 3.0


def test_get_bands_stats_empty():
    stats = get_bands_stats([], [])
    assert stats['total_bands'] == 0
    assert stats['avg_participants'] == 0.0


def test_get_band_status():
    assert get_band_status(True) == \
        'Группа доступна для прослушивания'
    assert get_band_status(False) == 'Группа уже занята'
