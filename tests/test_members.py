# tests/test_members.py
from models import Band
from models.band import add_band
from models.member import (
    add_member,
    count_members_for_band,
    evaluate_candidate,
    filter_members_by_band,
    find_member,
    iter_members_by_band,
    remove_member,
    sort_members,
)
from models.member import Member


def make_band(band_id=1):
    return Band(band_id, "Nirvana", "2026-06-06", "Бас-гитара", True)


def test_member_creation():
    band = make_band()
    member = Member(1, band, "Бас-гитара", 3)
    assert member.id == 1
    assert member.band is band
    assert member.band_id == 1
    assert member.instrument == "Бас-гитара"


def test_member_str():
    band = make_band()
    member = Member(1, band, "Бас-гитара", 3)
    assert "Бас-гитара" in str(member)
    assert "Nirvana" in str(member)


def test_member_from_data_to_dict():
    bands = [make_band(1)]
    data = {
        "id": 1,
        "band_id": 1,
        "instrument": "Бас-гитара",
        "experience_years": 3,
        "status": "Одобрено: Приглашаем на прослушивание!",
    }
    member = Member.from_data(data, bands)
    assert member.band is bands[0]
    assert member.to_dict() == data


def test_add_member():
    bands = [make_band(1)]
    members = []
    member = add_member(members, bands, 1, "Бас-гитара", 3)
    assert len(members) == 1
    assert member.band_id == 1
    assert member.id == 1
    assert member.band is bands[0]


def test_find_and_filter_member():
    bands = [make_band(1), make_band(2)]
    members = []
    add_member(members, bands, 1, "Бас-гитара", 3)
    add_member(members, bands, 2, "Гитара", 5)
    assert len(find_member(members, "бас")) == 1
    assert len(filter_members_by_band(members, 1)) == 1
    assert count_members_for_band(members, 1) == 1
    assert len(list(iter_members_by_band(members, 2))) == 1


def test_sort_members():
    bands = [make_band(1)]
    members = []
    add_member(members, bands, 1, "Гитара", 5)
    add_member(members, bands, 1, "Бас-гитара", 2)
    ordered = sort_members(members)
    assert ordered[0].experience_years == 2
    assert ordered[1].experience_years == 5


def test_remove_member():
    bands = [make_band(1)]
    members = []
    add_member(members, bands, 1, "Бас-гитара", 3)
    assert remove_member(members, 1) is True
    assert len(members) == 0
    assert remove_member(members, 999) is False


def test_evaluate_candidate():
    result = evaluate_candidate("Бас-гитара", "Бас-гитара", 3)
    assert result == "Одобрено: Приглашаем на прослушивание!"


def test_add_band_helper_kept():
    bands = []
    add_band(bands, "A", "2026-01-01", "Гитара", True)
    assert bands[0].name == "A"
