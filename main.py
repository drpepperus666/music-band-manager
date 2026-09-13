from datetime import date

# --- Базовые переменные проекта ---
band_name = "Nirvana"
foundation_date = date(2026, 6, 6)
required_instrument = "Бас-гитара"
is_active = True

# --- 1. Функция оценки кандидата на вступление в группу ---
def evaluate_candidate(candidate_instrument, needed_instrument, experience_years):
    experience_years = int(experience_years)
    if candidate_instrument != needed_instrument:
        return "Отказ: Нам нужен другой инструмент."
    elif experience_years < 2:
        return "Отказ: Недостаточно опыта (нужно минимум 2 года)."
    else:
        return "Одобрено: Приглашаем на прослушивание!"

# --- 2. Функция расчета стоимости репетиции для одного участника ---
def calculate_rehearsal_cost(total_cost, participants_count, has_discount):
    total_cost = float(total_cost)
    participants_count = int(participants_count)
    if participants_count <= 0:
        return 0.0
    
    if has_discount:
        # Отладка: breakpoint стоял на строке ниже.
        # При total_cost = 2000.0 в отладчике было видно final_cost = 2400.0
        # (наценка вместо скидки) — причина: множитель 1.2. Исправлено на 0.8 (скидка 20%).
        final_cost = total_cost * 0.8 
    else:
        final_cost = total_cost
        
    cost_per_person = final_cost / participants_count
    return cost_per_person

# --- 3. Функция проверки пригодности репетиционного помещения ---
def check_room_suitability(room_capacity, band_size, has_large_equipment):
    room_capacity = int(room_capacity)
    band_size = int(band_size)
    # Если у группы есть крупное оборудование (например, своя барабанная установка), 
    # оно условно занимает место еще двух человек.
    if has_large_equipment:
        effective_size = band_size + 2
    else:
        effective_size = band_size
        
    if effective_size > room_capacity:
        return "Помещение слишком маленькое, ищем другое."
    elif effective_size == room_capacity:
        return "Помещение подходит, но будет тесновато."
    else:
        return "Помещение отлично подходит!"


# --- Основной сценарий выполнения (вывод результатов в консоль) ---
print(f"--- Музыкальная группа: {band_name} ---")
print(f"Дата основания: {foundation_date}")
print(f"Сейчас ищем музыканта на инструмент: {required_instrument}")
print("Статус группы: " + str("активна" if is_active else "на паузе") + "\n")

# Тестирование первой функции
print("--- 1. Проверка кандидата ---")
cand_instrument = "Бас-гитара"
cand_exp = int("3")
print(f"Кандидат играет на: {cand_instrument}, Опыт: {cand_exp} года")
print("Вердикт:", evaluate_candidate(cand_instrument, required_instrument, cand_exp))
print()

# Тестирование второй функции
print("--- 2. Расчет стоимости репетиции ---")
rent_cost = float("2000.0")
members_present = int("4")
discount_status = True
print(f"Общая стоимость аренды: {rent_cost} руб.")
print(f"Пришло участников: {members_present}")
print(f"Наличие скидки 20%: {discount_status}")
print("С каждого участника:", calculate_rehearsal_cost(rent_cost, members_present, discount_status), "руб.")
print()

# Тестирование третьей функции
print("--- 3. Проверка помещения ---")
capacity = 5
band_members = 4
large_eq = True
print(f"Вместимость студии: {capacity} чел.")
print(f"Размер группы: {band_members} чел.")
print(f"Наличие крупного оборудования: {large_eq}")
print("Статус:", check_room_suitability(capacity, band_members, large_eq))