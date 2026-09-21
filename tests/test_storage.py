# tests/test_storage.py
from storage import load_bands, save_bands, load_rehearsals, save_rehearsals


def test_load_missing_file_returns_empty(tmp_path):
    missing = str(tmp_path / "no_such_file.json")
    assert load_bands(missing) == []
    assert load_rehearsals(missing) == []


def test_load_invalid_json_returns_empty(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not valid json", encoding="utf-8")
    assert load_bands(str(bad)) == []


def test_save_load_bands_roundtrip(tmp_path):
    path = str(tmp_path / "bands.json")
    bands = [{'id': 1, 'name': 'A', 'members': [], 'is_active': True}]
    save_bands(path, bands)
    assert load_bands(path) == bands


def test_save_load_rehearsals_roundtrip(tmp_path):
    path = str(tmp_path / "rehearsals.json")
    data = [{'id': 1, 'band_id': 1,
             'rehearsal_date': '2026-09-15', 'participants': 4}]
    save_rehearsals(path, data)
    assert load_rehearsals(path) == data
