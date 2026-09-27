"""Класс Band и функции работы с коллекцией групп (ПР3)."""

from typing import TYPE_CHECKING, Iterator, Optional

if TYPE_CHECKING:
    from .rehearsal import Rehearsal


class Band:
    """Группа (музыкальный коллектив)."""

    def __init__(
        self,
        band_id: int,
        name: str,
        foundation_date: str,
        required_instrument: str,
        is_active: bool,
        members: Optional[list] = None,
    ) -> None:
        """Создать объект группы."""
        self.id = int(band_id)
        self.name = name
        self.foundation_date = foundation_date
        self.required_instrument = required_instrument
        self.is_active = bool(is_active)
        self.members = list(members) if members is not None else []

    def is_suitable_for(self, min_capacity: int) -> bool:
        """Проверить, хватает ли участников группы."""
        return len(self.members) >= int(min_capacity)

    @staticmethod
    def validate_capacity(capacity: int) -> bool:
        """Проверить корректность вместимости."""
        return int(capacity) >= 0

    @classmethod
    def from_data(cls, data: dict) -> "Band":
        """Создать группу из словаря (загрузка JSON)."""
        return cls(
            band_id=data["id"],
            name=data["name"],
            foundation_date=data.get("foundation_date", ""),
            required_instrument=data.get("required_instrument", ""),
            is_active=data.get("is_active", False),
            members=data.get("members", []),
        )

    def to_dict(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "foundation_date": self.foundation_date,
            "required_instrument": self.required_instrument,
            "is_active": self.is_active,
            "members": list(self.members),
        }

    def __str__(self) -> str:
        """Вернуть строковое представление группы."""
        status = get_band_status(self.is_active)
        return (
            f"{self.name} ({self.required_instrument}), "
            f"участников: {len(self.members)}, {status}"
        )


def add_band(
    bands: list,
    name: str,
    foundation_date: str,
    required_instrument: str,
    is_active: bool,
) -> Band:
    """Создать объект Band и добавить его в коллекцию."""
    band_id = max((b.id for b in bands), default=0) + 1
    band = Band(
        band_id=band_id,
        name=name,
        foundation_date=foundation_date,
        required_instrument=required_instrument,
        is_active=is_active,
        members=[],
    )
    bands.append(band)
    return band


def find_band(bands: list, query: str) -> list:
    """Найти группы по подстроке названия."""
    return [b for b in bands if query.lower() in b.name.lower()]


def find_band_by_id(bands: list, band_id: int) -> Optional[Band]:
    """Найти группу по идентификатору."""
    for band in bands:
        if band.id == int(band_id):
            return band
    return None


def check_band_capacity(
    bands: list,
    band_id: int,
    min_capacity: int,
) -> bool:
    """Проверить вместимость группы через метод объекта."""
    band = find_band_by_id(bands, band_id)
    if band is None:
        return False
    return band.is_suitable_for(min_capacity)


def filter_bands_by_active(bands: list, active: bool = True) -> list:
    """Отобрать группы по статусу активности."""
    return [b for b in bands if b.is_active == active]


def iter_active_bands(bands: list) -> Iterator[Band]:
    """Генератор активных групп."""
    for band in bands:
        if band.is_active:
            yield band


def get_bands_stats(bands: list, rehearsals: "list[Rehearsal]") -> dict:
    """Посчитать статистику по группам и репетициям."""
    total_bands = len(bands)
    active_bands = sum(1 for b in bands if b.is_active)
    total_rehearsals = len(rehearsals)
    total_parts = sum(r.participants for r in rehearsals)
    if total_rehearsals:
        avg_parts = total_parts / total_rehearsals
    else:
        avg_parts = 0.0
    return {
        "total_bands": total_bands,
        "active_bands": active_bands,
        "total_rehearsals": total_rehearsals,
        "avg_participants": avg_parts,
    }


def sort_bands(bands: list, key: str = "name") -> list:
    """Отсортировать группы по атрибуту."""
    return sorted(bands, key=lambda b: getattr(b, key, ""))


def get_band_status(is_active: bool) -> str:
    """Вернуть текстовый статус группы (из ПР1)."""
    if is_active:
        return "Группа доступна для прослушивания"
    return "Группа уже занята"


def show_bands(bands: list) -> None:
    """Вывести список групп через __str__."""
    if not bands:
        print("Групп пока нет.")
        return
    for band in bands:
        print(f"  ID: {band.id}, {band}")
