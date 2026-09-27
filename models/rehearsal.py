"""Класс Rehearsal и функции работы с репетициями (ПР3)."""

from typing import Optional, Union

from .band import Band, find_band_by_id
from .room import Room


class Rehearsal:
    """Репетиция группы (бронирование)."""

    def __init__(
        self,
        rehearsal_id: int,
        band: Band,
        rehearsal_date: str,
        participants: int,
        is_cancelled: bool = False,
    ) -> None:
        """Создать объект репетиции."""
        self.id = int(rehearsal_id)
        self.band = band
        self.rehearsal_date = rehearsal_date
        self.participants = int(participants)
        self.is_cancelled = bool(is_cancelled)

    def cancel(self) -> None:
        """Отменить репетицию (без удаления из коллекции)."""
        self.is_cancelled = True

    @property
    def band_id(self) -> Optional[int]:
        """Вернуть идентификатор связанной группы."""
        return self.band.id if self.band is not None else None

    @classmethod
    def from_data(cls, data: dict, bands: list) -> Optional["Rehearsal"]:
        """Создать репетицию из словаря, связав с объектом Band."""
        band = find_band_by_id(bands, data.get("band_id"))
        if band is None:
            return None
        return cls(
            rehearsal_id=data["id"],
            band=band,
            rehearsal_date=data.get("rehearsal_date", ""),
            participants=data.get("participants", 0),
            is_cancelled=data.get("is_cancelled", False),
        )

    def to_dict(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "band_id": self.band_id,
            "rehearsal_date": self.rehearsal_date,
            "participants": self.participants,
            "is_cancelled": self.is_cancelled,
        }

    def __str__(self) -> str:
        """Вернуть строковое представление репетиции."""
        state = "отменена" if self.is_cancelled else "активна"
        band_name = self.band.name if self.band is not None else "—"
        return (
            f"Репетиция {self.id} ({band_name}, {self.rehearsal_date}, "
            f"участников: {self.participants}, {state})"
        )


def calculate_rehearsal_cost(
    total_cost: float,
    participants_count: int,
    has_discount: bool,
) -> float:
    """Рассчитать стоимость репетиции для одного участника (из ПР1)."""
    total_cost = float(total_cost)
    participants_count = int(participants_count)
    if participants_count <= 0:
        return 0.0
    if has_discount:
        final_cost = total_cost * 0.8
    else:
        final_cost = total_cost
    return final_cost / participants_count


def check_room_suitability(
    room_capacity: int,
    band_size: int,
    has_large_equipment: bool,
) -> str:
    """Проверить пригодность помещения (из ПР1, через Room)."""
    room = Room(room_id=0, name="Студия", capacity=int(room_capacity))
    suitable = room.is_suitable_for(int(band_size), has_large_equipment)
    effective = int(band_size) + (2 if has_large_equipment else 0)
    if not suitable:
        return "Помещение слишком маленькое, ищем другое."
    elif effective == room.capacity:
        return "Помещение подходит, но будет тесновато."
    else:
        return "Помещение отлично подходит!"


def _band_key(band: Union[Band, int]) -> Optional[int]:
    """Привести Band или band_id к идентификатору."""
    if isinstance(band, Band):
        return band.id
    return int(band)


def is_band_available(
    rehearsals: list,
    band: Union[Band, int],
    rehearsal_date: str,
) -> bool:
    """Проверить, свободна ли группа на дату (активные репетиции)."""
    band_id = _band_key(band)
    for r in rehearsals:
        if r.is_cancelled:
            continue
        if r.band_id == band_id and r.rehearsal_date == rehearsal_date:
            return False
    return True


def create_rehearsal(
    rehearsals: list,
    band: Union[Band, int],
    bands: Optional[list] = None,
    rehearsal_date: str = "",
    participants: int = 0,
) -> Optional[Rehearsal]:
    """Создать объект Rehearsal, если дата свободна."""
    if isinstance(band, Band):
        band_obj = band
    elif bands is not None:
        band_obj = find_band_by_id(bands, band)
        if band_obj is None:
            return None
    else:
        return None
    if not is_band_available(rehearsals, band_obj, rehearsal_date):
        return None
    rehearsal_id = max((r.id for r in rehearsals), default=0) + 1
    rehearsal = Rehearsal(
        rehearsal_id=rehearsal_id,
        band=band_obj,
        rehearsal_date=rehearsal_date,
        participants=int(participants),
    )
    rehearsals.append(rehearsal)
    return rehearsal


def add_rehearsal(
    rehearsals: list,
    band: Union[Band, int],
    rehearsal_date: str = "",
    participants: int = 0,
    bands: Optional[list] = None,
) -> Optional[Rehearsal]:
    """Добавить репетицию (совместимая обертка над create_rehearsal)."""
    if isinstance(band, Band):
        return create_rehearsal(
            rehearsals, band, None, rehearsal_date, participants
        )
    return create_rehearsal(
        rehearsals, band, bands, rehearsal_date, participants
    )


def cancel_rehearsal(rehearsals: list, rehearsal_id: int) -> bool:
    """Отменить репетицию через метод объекта (без удаления)."""
    for r in rehearsals:
        if r.id == int(rehearsal_id):
            r.cancel()
            return True
    return False


def find_rehearsal_by_id(
    rehearsals: list,
    rehearsal_id: int,
) -> Optional[Rehearsal]:
    """Найти репетицию по идентификатору."""
    for r in rehearsals:
        if r.id == int(rehearsal_id):
            return r
    return None


def get_rehearsal_status(is_available: bool) -> str:
    """Вернуть текстовый статус репетиции (из ПР1)."""
    if is_available:
        return "Репетиция доступна для бронирования"
    return "Репетиция уже занята"


def show_rehearsals(rehearsals: list) -> None:
    """Вывести список репетиций через __str__."""
    if not rehearsals:
        print("Репетиций пока нет.")
        return
    for r in rehearsals:
        print(f"  {r}")
