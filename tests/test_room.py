# tests/test_room.py
from models import Room


def test_room_creation():
    room = Room(1, "Студия А", 5)
    assert room.id == 1
    assert room.name == "Студия А"
    assert room.capacity == 5


def test_room_is_suitable_for():
    room = Room(1, "Студия А", 5)
    assert room.is_suitable_for(4) is True
    assert room.is_suitable_for(5) is True
    assert room.is_suitable_for(6) is False
    assert room.is_suitable_for(4, True) is False


def test_room_validate_capacity():
    assert Room.validate_capacity(5) is True


def test_room_str():
    room = Room(1, "Студия А", 5)
    assert "Студия А" in str(room)
