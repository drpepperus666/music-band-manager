"""Функции работы с участниками (сущность Member).

Связь сущностей:
  Member.band_id -> Band.id (много участников к одной группе).
  Rehearsal.band_id -> Band.id (много репетиций к одной группе).
"""


def evaluate_candidate(candidate_instrument: str,
                       needed_instrument: str,
                       experience_years: int) -> str:
    """Оценить кандидата на вступление в группу (из ПР1)."""
    experience_years = int(experience_years)
    if candidate_instrument != needed_instrument:
        return 'Отказ: Нам нужен другой инструмент.'
    elif experience_years < 2:
        return 'Отказ: Недостаточно опыта (нужно минимум 2 года).'
    else:
        return 'Одобрено: Приглашаем на прослушивание!'


def add_member(members: list[dict], band_id: int,
               instrument: str, experience_years: int) -> dict:
    """Добавить участника и привязать его к группе через band_id."""
    member_id = max((m['id'] for m in members), default=0) + 1
    member = {
        'id': member_id,
        'band_id': int(band_id),
        'instrument': instrument,
        'experience_years': int(experience_years),
        'status': 'Кандидат добавлен',
    }
    members.append(member)
    return member


def find_member(members: list[dict], query: str) -> list[dict]:
    """Найти участников по подстроке названия инструмента."""
    return [m for m in members if query.lower() in m['instrument'].lower()]


def filter_members_by_band(members: list[dict],
                           band_id: int) -> list[dict]:
    """Отобрать участников одной группы по band_id."""
    return [m for m in members if m['band_id'] == band_id]


def iter_members_by_band(members: list[dict], band_id: int):
    """Генератор участников одной группы (пример yield)."""
    for member in members:
        if member['band_id'] == band_id:
            yield member


def sort_members(members: list[dict],
                 key: str = 'experience_years') -> list[dict]:
    """Отсортировать участников по ключу (через lambda)."""
    return sorted(members, key=lambda m: m.get(key, ''))


def remove_member(members: list[dict], member_id: int) -> bool:
    """Удалить участника по id. True, если найден и удален."""
    for i, member in enumerate(members):
        if member['id'] == member_id:
            members.pop(i)
            return True
    return False


def count_members_for_band(members: list[dict], band_id: int) -> int:
    """Посчитать число участников группы (связь Member -> Band)."""
    count = 0
    for member in members:
        if member['band_id'] == band_id:
            count += 1
    return count
