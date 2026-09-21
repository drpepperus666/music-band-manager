# tests/test_members.py
from members import (
    add_member,
    find_member,
    filter_members_by_band,
    iter_members_by_band,
    sort_members,
    remove_member,
    count_members_for_band,
    evaluate_candidate,
)


def test_add_member():
    members = []
    member = add_member(members, 1, "Бас-гитара", 3)
    assert len(members) == 1
    assert member['band_id'] == 1
    assert member['id'] == 1


def test_find_and_filter_member():
    members = []
    add_member(members, 1, "Бас-гитара", 3)
    add_member(members, 2, "Гитара", 5)
    assert len(find_member(members, "бас")) == 1
    assert len(filter_members_by_band(members, 1)) == 1
    assert count_members_for_band(members, 1) == 1
    assert len(list(iter_members_by_band(members, 2))) == 1


def test_sort_members():
    members = []
    add_member(members, 1, "Гитара", 5)
    add_member(members, 1, "Бас-гитара", 2)
    ordered = sort_members(members)
    assert ordered[0]['experience_years'] == 2
    assert ordered[1]['experience_years'] == 5


def test_remove_member():
    members = []
    add_member(members, 1, "Бас-гитара", 3)
    assert remove_member(members, 1) is True
    assert len(members) == 0
    assert remove_member(members, 999) is False


def test_evaluate_candidate():
    result = evaluate_candidate("Бас-гитара", "Бас-гитара", 3)
    assert result == "Одобрено: Приглашаем на прослушивание!"
