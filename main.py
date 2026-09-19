from bands import (
    find_band,
    check_band_capacity,
    evaluate_candidate,
)
from rehearsals import (
    calculate_rehearsal_cost,
    check_room_suitability,
    add_rehearsal,
    is_band_available,
    cancel_rehearsal,
    get_rehearsal_status,
)
from storage import (
    load_bands,
    save_bands,
    load_members,
    save_members,
    load_rehearsals,
    save_rehearsals,
)
from utils import input_int, input_date, input_string


def show_bands(bands: list[dict]) -> None:
    """Вывести список групп."""
    if not bands:
        print('Групп пока нет.')
        return
    for band in bands:
        print(f"  ID: {band['id']}, Название: {band['name']}, "
              f"Инструмент: {band['required_instrument']}, "
              f"Активна: {band['is_active']}")


def show_rehearsals(rehearsals: list[dict]) -> None:
    """Вывести список репетиций."""
    if not rehearsals:
        print('Репетиций пока нет.')
        return
    for r in rehearsals:
        print(f"  ID: {r['id']}, Группа ID: {r['band_id']}, "
              f"Дата: {r['rehearsal_date']}, Участники: {r['participants']}")


def main() -> None:
    """Точка запуска приложения: меню и вызов функций."""
    bands = load_bands('data/bands.json')
    members = load_members('data/members.json')
    rehearsals = load_rehearsals('data/rehearsals.json')

    while True:
        print('\n=== Система организации музыкальных групп ===')
        print('1. Показать все группы')
        print('2. Найти группу по названию')
        print('3. Проверить вместимость группы')
        print('4. Проверить доступность на дату репетиции')
        print('5. Забронировать репетицию')
        print('6. Отменить бронирование репетиции')
        print('7. Показать репетиции')
        print('8. Оценить кандидата')
        print('9. Рассчитать стоимость репетиции')
        print('10. Проверить пригодность помещения')
        print('0. Выход')

        choice = input_int('Выберите действие: ')

        if choice == 1:
            show_bands(bands)
        elif choice == 2:
            query = input_string('Введите название группы для поиска: ')
            results = find_band(bands, query)
            show_bands(results)
        elif choice == 3:
            band_id = input_int('Введите ID группы: ')
            min_cap = input_int('Введите минимальную вместимость: ')
            result = check_band_capacity(bands, band_id, min_cap)
            print(f'Результат: {result}')
        elif choice == 4:
            band_id = input_int('Введите ID группы: ')
            d = input_date('Введите дату (YYYY-MM-DD): ')
            available = is_band_available(rehearsals, band_id, d.isoformat())
            print(get_rehearsal_status(available))
        elif choice == 5:
            band_id = input_int('Введите ID группы: ')
            d = input_date('Введите дату репетиции (YYYY-MM-DD): ')
            participants = input_int('Введите количество участников: ')
            if is_band_available(rehearsals, band_id, d.isoformat()):
                add_rehearsal(rehearsals, band_id, d.isoformat(),
                              participants)
                save_rehearsals('data/rehearsals.json', rehearsals)
                print('Репетиция успешно забронирована!')
            else:
                print('Группа уже занята на эту дату!')
        elif choice == 6:
            r_id = input_int('Введите ID репетиции для отмены: ')
            if cancel_rehearsal(rehearsals, r_id):
                save_rehearsals('data/rehearsals.json', rehearsals)
                print('Репетиция отменена.')
            else:
                print('Репетиция с таким ID не найдена.')
        elif choice == 7:
            show_rehearsals(rehearsals)
        elif choice == 8:
            cand_instrument = input_string('Инструмент кандидата: ')
            needed = input_string('Требуемый инструмент: ')
            exp = input_int('Опыт в годах: ')
            print(evaluate_candidate(cand_instrument, needed, exp))
        elif choice == 9:
            total = float(input('Общая стоимость аренды: '))
            count = input_int('Количество участников: ')
            discount = input_string('Скидка есть? (да/нет): ').lower() == 'да'
            print(f'С каждого: '
                  f'{calculate_rehearsal_cost(total, count, discount)} руб.')
        elif choice == 10:
            cap = input_int('Вместимость студии: ')
            size = input_int('Размер группы: ')
            large_eq = input_string(
                'Крупное оборудование? (да/нет): ').lower() == 'да'
            print(check_room_suitability(cap, size, large_eq))
        elif choice == 0:
            save_bands('data/bands.json', bands)
            save_members('data/members.json', members)
            save_rehearsals('data/rehearsals.json', rehearsals)
            print('Данные сохранены. Выход.')
            break
        else:
            print('Неверный выбор. Попробуйте снова.')


if __name__ == '__main__':
    main()
