def add_band(bands: list[dict], name: str, foundation_date: str,
             required_instrument: str, is_active: bool) -> None:
    """Добавить группу в список bands."""
    band_id = max((b['id'] for b in bands), default=0) + 1
    bands.append({
        'id': band_id,
        'name': name,
        'foundation_date': foundation_date,
        'required_instrument': required_instrument,
        'is_active': is_active,
    })


def find_band(bands: list[dict], query: str) -> list[dict]:
    """Найти группы по подстроке названия."""
    return [b for b in bands if query.lower() in b['name'].lower()]


def check_band_capacity(bands: list[dict], band_id: int,
                        min_capacity: int) -> bool:
    """Проверить, что группа с данным id существует и имеет
    вместимость >= min_capacity."""
    for band in bands:
        if band['id'] == band_id:
            return len(band.get('members', [])) >= min_capacity
    return False


def filter_bands_by_active(bands: list[dict], active: bool = True) \
        -> list[dict]:
    """Отобрать группы по статусу активности."""
    return [b for b in bands if b['is_active'] == active]


def sort_bands(bands: list[dict], key: str = 'name') -> list[dict]:
    """Отсортировать группы по указанному ключу."""
    return sorted(bands, key=lambda b: b.get(key, ''))


def evaluate_candidate(candidate_instrument: str, needed_instrument: str,
                       experience_years: int) -> str:
    """Оценить кандидата на вступление в группу (из ПР1)."""
    experience_years = int(experience_years)
    if candidate_instrument != needed_instrument:
        return 'Отказ: Нам нужен другой инструмент.'
    elif experience_years < 2:
        return 'Отказ: Недостаточно опыта (нужно минимум 2 года).'
    else:
        return 'Одобрено: Приглашаем на прослушивание!'


def get_band_status(is_available: bool) -> str:
    """Вернуть текстовый статус группы (из ПР1)."""
    if is_available:
        return 'Группа доступна для прослушивания'
    return 'Группа уже занята'
