# tests/test_storage.py
import json

from models.band import Band
from storage import (
    load_bands,
    load_members,
    load_rehearsals,
    save_bands,
    save_members,
    save_rehearsals,
)


def test_load_missing_file_returns_empty(tmp_path):
    missing = str(tmp_path / "no_such_file.json")
    assert load_bands(missing) == []
    assert load_rehearsals(missing, []) == []
    assert load_members(missing, []) == []


def test_load_invalid_json_returns_empty(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not valid json", encoding="utf-8")
    assert load_bands(str(bad)) == []


def test_save_load_bands_roundtrip(tmp_path):
    path = str(tmp_path / "bands.json")
    bands = [Band(1, "A", "2026-01-01", "Гитара", True, members=[])]
    save_bands(path, bands)
    loaded = load_bands(path)
    assert len(loaded) == 1
    assert loaded[0].name == "A"
    assert loaded[0].to_dict() == bands[0].to_dict()


def test_save_load_rehearsals_roundtrip(tmp_path):
    from models.rehearsal import Rehearsal

    bands_path = str(tmp_path / "bands.json")
    bands = [Band(1, "A", "2026-01-01", "Гитара", True, members=[])]
    save_bands(bands_path, bands)
    loaded_bands = load_bands(bands_path)

    path = str(tmp_path / "rehearsals.json")
    rehearsals = [Rehearsal(1, loaded_bands[0], "2026-09-15", 4)]
    save_rehearsals(path, rehearsals)
    raw = json.loads(open(path, encoding="utf-8").read())
    assert raw[0]["band_id"] == 1
    assert "band" not in raw[0]
    loaded = load_rehearsals(path, loaded_bands)
    assert len(loaded) == 1
    assert loaded[0].band is loaded_bands[0]
    assert loaded[0].is_cancelled is False


def test_save_load_members_link(tmp_path):
    bands = [Band(1, "A", "2026-01-01", "Гитара", True, members=[])]
    path = str(tmp_path / "members.json")
    from models.member import Member

    members = [Member(1, bands[0], "Гитара", 3)]
    save_members(path, members)
    loaded = load_members(path, bands)
    assert loaded[0].band is bands[0]
    assert loaded[0].band_id == 1


def test_load_rehearsal_skips_missing_band(tmp_path):
    path = str(tmp_path / "rehearsals.json")
    raw = [
        {
            "id": 1,
            "band_id": 999,
            "rehearsal_date": "2026-09-15",
            "participants": 4,
            "is_cancelled": False,
        }
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(raw, f)
    assert load_rehearsals(path, []) == []
