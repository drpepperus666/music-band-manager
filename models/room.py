"""Класс Room — репетиционное помещение (ПР3, лайт-версия)."""

from typing import Optional


class Room:
    """Помещение для репетиций."""

    def __init__(self, room_id: int, name: str, capacity: int) -> None:
        """Создать объект помещения."""
        self.id = int(room_id)
        self.name = name
        self.capacity = int(capacity)

    def is_suitable_for(
        self,
        band_size: int,
        has_large_equipment: bool = False,
    ) -> bool:
        """Проверить, подходит ли помещение по вместимости."""
        effective_size = int(band_size) + (2 if has_large_equipment else 0)
        return self.capacity >= effective_size

    @staticmethod
    def validate_capacity(capacity: int) -> bool:
        """Проверить корректность вместимости."""
        return int(capacity) >= 0

    @classmethod
    def from_data(cls, data: dict) -> "Room":
        """Создать помещение из словаря."""
        return cls(
            room_id=data["id"],
            name=data.get("name", ""),
            capacity=data.get("capacity", 0),
        )

    def to_dict(self) -> dict:
        """Преобразовать объект в словарь."""
        return {
            "id": self.id,
            "name": self.name,
            "capacity": self.capacity,
        }

    def __str__(self) -> str:
        """Вернуть строковое представление помещения."""
        return f"{self.name}, вместимость: {self.capacity} чел."


def find_room_by_id(rooms: list["Room"], room_id: int) -> Optional[Room]:
    """Найти помещение по идентификатору."""
    for room in rooms:
        if room.id == int(room_id):
            return room
    return None
