"""Класс Member и функции работы с участниками (ПР3)."""

from typing import Iterator, Optional

from .band import Band, find_band_by_id


class Member:
    """Участник / кандидат музыкальной группы."""

    def __init__(
        self,
        member_id: int,
        band: Optional[Band],
        instrument: str,
        experience_years: int,
        status: str = "Кандидат добавлен",
    ) -> None:
        """Создать объект участника."""
        self.id = int(member_id)
        self.band = band
        self.instrument = instrument
        self.experience_years = int(experience_years)
        self.status = status

    @property
    def band_id(self) -> Optional[int]:
        """Вернуть идентификатор связанной группы."""
        return self.band.id if self.band is not None else None

    @classmethod
    def from_data(cls, data: dict, bands: list) -> "Member":
        """Создать участника из словаря, связав с объектом Band."""
        band = find_band_by_id(bands, data.get("band_id"))
        return cls(
            member_id=data["id"],
            band=band,
            instrument=data.get("instrument", ""),
            experience_years=data.get("experience_years", 0),
            status=data.get("status", "Кандидат добавлен"),
        )

    def to_dict(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "band_id": self.band_id,
            "instrument": self.instrument,
            "experience_years": self.experience_years,
            "status": self.status,
        }

    def __str__(self) -> str:
        """Вернуть строковое представление участника."""
        band_name = self.band.name if self.band is not None else "—"
        return (
            f"Участник {self.id} ({self.instrument}, "
            f"опыт {self.experience_years} г., группа: {band_name})"
        )


def evaluate_candidate(
    candidate_instrument: str,
    needed_instrument: str,
    experience_years: int,
) -> str:
    """Оценить кандидата на вступление в группу (из ПР1)."""
    experience_years = int(experience_years)
    if candidate_instrument != needed_instrument:
        return "Отказ: Нам нужен другой инструмент."
    elif experience_years < 2:
        return "Отказ: Недостаточно опыта (нужно минимум 2 года)."
    else:
        return "Одобрено: Приглашаем на прослушивание!"


def add_member(
    members: list,
    bands: list,
    band_id: int,
    instrument: str,
    experience_years: int,
) -> Member:
    """Создать объект Member, связав с объектом Band."""
    member_id = max((m.id for m in members), default=0) + 1
    band = find_band_by_id(bands, band_id)
    member = Member(
        member_id=member_id,
        band=band,
        instrument=instrument,
        experience_years=experience_years,
    )
    members.append(member)
    return member


def find_member(members: list, query: str) -> list:
    """Найти участников по подстроке названия инструмента."""
    return [m for m in members if query.lower() in m.instrument.lower()]


def find_member_by_id(members: list, member_id: int) -> Optional[Member]:
    """Найти участника по идентификатору."""
    for member in members:
        if member.id == int(member_id):
            return member
    return None


def filter_members_by_band(members: list, band_id: int) -> list:
    """Отобрать участников одной группы."""
    return [m for m in members if m.band_id == int(band_id)]


def iter_members_by_band(members: list, band_id: int) -> Iterator[Member]:
    """Генератор участников одной группы."""
    for member in members:
        if member.band_id == int(band_id):
            yield member


def sort_members(members: list, key: str = "experience_years") -> list:
    """Отсортировать участников по атрибуту (через lambda)."""
    return sorted(members, key=lambda m: getattr(m, key, ""))


def remove_member(members: list, member_id: int) -> bool:
    """Удалить участника по id. True, если найден и удален."""
    for i, member in enumerate(members):
        if member.id == int(member_id):
            members.pop(i)
            return True
    return False


def count_members_for_band(members: list, band_id: int) -> int:
    """Посчитать число участников группы (связь Member -> Band)."""
    count = 0
    for member in members:
        if member.band_id == int(band_id):
            count += 1
    return count


def show_members(members: list) -> None:
    """Вывести список участников через __str__."""
    if not members:
        print("Участников пока нет.")
        return
    for member in members:
        print(f"  {member}, статус: {member.status}")
