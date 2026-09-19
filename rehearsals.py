def calculate_rehearsal_cost(total_cost: float, participants_count: int,
                             has_discount: bool) -> float:
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


def check_room_suitability(room_capacity: int, band_size: int,
                           has_large_equipment: bool) -> str:
    """Проверить пригодность репетиционного помещения (из ПР1)."""
    room_capacity = int(room_capacity)
    band_size = int(band_size)
    if has_large_equipment:
        effective_size = band_size + 2
    else:
        effective_size = band_size
    if effective_size > room_capacity:
        return 'Помещение слишком маленькое, ищем другое.'
    elif effective_size == room_capacity:
        return 'Помещение подходит, но будет тесновато.'
    else:
        return 'Помещение отлично подходит!'


def add_rehearsal(rehearsals: list[dict], band_id: int,
                  rehearsal_date: str, participants: int) -> None:
    """Добавить запись о репетиции."""
    rehearsal_id = max((r['id'] for r in rehearsals), default=0) + 1
    rehearsals.append({
        'id': rehearsal_id,
        'band_id': band_id,
        'rehearsal_date': rehearsal_date,
        'participants': participants,
    })


def is_band_available(rehearsals: list[dict], band_id: int,
                      rehearsal_date: str) -> bool:
    """Проверить, свободно ли помещение группы на дату репетиции."""
    for r in rehearsals:
        if r['band_id'] == band_id and r['rehearsal_date'] == rehearsal_date:
            return False
    return True


def cancel_rehearsal(rehearsals: list[dict], rehearsal_id: int) -> bool:
    """Отменить репетицию по id. Возвращает True, если найдена и удалена."""
    for i, r in enumerate(rehearsals):
        if r['id'] == rehearsal_id:
            rehearsals.pop(i)
            return True
    return False


def get_rehearsal_status(is_available: bool) -> str:
    """Вернуть текстовый статус репетиции (из ПР1)."""
    if is_available:
        return 'Репетиция доступна для бронирования'
    return 'Репетиция уже занята'
