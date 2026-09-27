"""Точка запуска приложения (ПР3, объектная модель)."""

from models import Band, Member, Rehearsal
from models.band import (
    check_band_capacity,
    filter_bands_by_active,
    find_band,
    find_band_by_id,
    get_bands_stats,
    iter_active_bands,
    show_bands,
    sort_bands,
)
from models.member import (
    add_member,
    count_members_for_band,
    evaluate_candidate,
    filter_members_by_band,
    find_member,
    show_members,
    sort_members,
)
from models.rehearsal import (
    calculate_rehearsal_cost,
    cancel_rehearsal,
    check_room_suitability,
    create_rehearsal,
    get_rehearsal_status,
    is_band_available,
    show_rehearsals,
)
from storage import (
    load_bands,
    load_members,
    load_rehearsals,
    save_bands,
    save_members,
    save_rehearsals,
)
from utils import input_date, input_float, input_int, input_string


def show_stats(bands: list[Band], rehearsals: list[Rehearsal]) -> None:
    """Вывести статистику проекта."""
    stats = get_bands_stats(bands, rehearsals)
    print(f"  Всего групп: {stats['total_bands']}")
    print(f"  Активных групп: {stats['active_bands']}")
    print(f"  Всего репетиций: {stats['total_rehearsals']}")
    print(f"  Среднее число участников: {stats['avg_participants']:.1f}")


def create_new_rehearsal(
    rehearsals: list[Rehearsal], bands: list[Band]
) -> None:
    """Сценарий бронирования: Band + дата -> объект Rehearsal."""
    band_id = input_int("Введите ID группы: ")
    band = find_band_by_id(bands, band_id)
    if band is None:
        print("Группа с таким ID не найдена.")
        return
    d = input_date("Введите дату репетиции (YYYY-MM-DD): ")
    participants = input_int("Введите количество участников: ")
    rehearsal = create_rehearsal(
        rehearsals, band, None, d.isoformat(), participants
    )
    if rehearsal is None:
        print("Группа уже занята на эту дату!")
        return
    save_rehearsals("data/rehearsals.json", rehearsals)
    print(f"Репетиция забронирована с ID {rehearsal.id}: {rehearsal}")


def main() -> None:
    """Запустить приложение: меню и операции над объектами."""
    bands: list[Band] = load_bands("data/bands.json")
    members: list[Member] = load_members("data/members.json", bands)
    rehearsals: list[Rehearsal] = load_rehearsals(
        "data/rehearsals.json", bands
    )

    while True:
        print("\n=== Система организации музыкальных групп ===")
        print("1. Показать все группы")
        print("2. Найти группу по названию")
        print("3. Проверить вместимость группы")
        print("4. Проверить доступность на дату репетиции")
        print("5. Забронировать репетицию")
        print("6. Отменить бронирование репетиции")
        print("7. Показать репетиции")
        print("8. Оценить кандидата")
        print("9. Рассчитать стоимость репетиции")
        print("10. Проверить пригодность помещения")
        print("11. Показать группы отсортированные по названию")
        print("12. Показать только активные группы")
        print("13. Показать статистику")
        print("14. Показать участников группы")
        print("15. Добавить участника в группу")
        print("0. Выход")

        choice = input_int("Выберите действие: ")

        if choice == 1:
            show_bands(bands)
        elif choice == 2:
            query = input_string("Введите название группы для поиска: ")
            show_bands(find_band(bands, query))
        elif choice == 3:
            band_id = input_int("Введите ID группы: ")
            min_cap = input_int("Введите минимальную вместимость: ")
            result = check_band_capacity(bands, band_id, min_cap)
            print(f"Результат: {result}")
        elif choice == 4:
            band_id = input_int("Введите ID группы: ")
            band = find_band_by_id(bands, band_id)
            if band is None:
                print("Группа с таким ID не найдена.")
                continue
            d = input_date("Введите дату (YYYY-MM-DD): ")
            available = is_band_available(
                rehearsals, band, d.isoformat()
            )
            print(get_rehearsal_status(available))
        elif choice == 5:
            create_new_rehearsal(rehearsals, bands)
        elif choice == 6:
            r_id = input_int("Введите ID репетиции для отмены: ")
            if cancel_rehearsal(rehearsals, r_id):
                save_rehearsals("data/rehearsals.json", rehearsals)
                print("Репетиция отменена (статус is_cancelled).")
            else:
                print("Репетиция с таким ID не найдена.")
        elif choice == 7:
            show_rehearsals(rehearsals)
        elif choice == 8:
            cand_instrument = input_string("Инструмент кандидата: ")
            band_id = input_int("ID группы (для требования): ")
            band = find_band_by_id(bands, band_id)
            needed = band.required_instrument if band else input_string(
                "Требуемый инструмент: "
            )
            exp = input_int("Опыт в годах: ")
            print(evaluate_candidate(cand_instrument, needed, exp))
        elif choice == 9:
            total = input_float("Общая стоимость аренды: ")
            count = input_int("Количество участников: ")
            discount = input_string("Скидка есть? (да/нет): ").lower()
            print(
                "С каждого: "
                f"{calculate_rehearsal_cost(total, count, discount == 'да')}"
                " руб."
            )
        elif choice == 10:
            cap = input_int("Вместимость студии: ")
            size = input_int("Размер группы: ")
            large_eq = input_string(
                "Крупное оборудование? (да/нет): "
            ).lower() == "да"
            print(check_room_suitability(cap, size, large_eq))
        elif choice == 11:
            show_bands(sort_bands(bands))
        elif choice == 12:
            active = filter_bands_by_active(bands, True)
            print("Активные группы (через генератор):")
            show_bands(list(iter_active_bands(bands)))
            print(f"Всего активных: {len(active)}")
        elif choice == 13:
            show_stats(bands, rehearsals)
        elif choice == 14:
            band_id = input_int("Введите ID группы: ")
            group_members = filter_members_by_band(members, band_id)
            print(
                f"Участников в группе {band_id}: "
                f"{count_members_for_band(members, band_id)}"
            )
            show_members(sort_members(group_members))
        elif choice == 15:
            band_id = input_int("Введите ID группы: ")
            if find_band_by_id(bands, band_id) is None:
                print("Группа с таким ID не найдена.")
                continue
            instr = input_string("Инструмент участника: ")
            exp = input_int("Опыт в годах: ")
            new_member: Member = add_member(
                members, bands, band_id, instr, exp
            )
            save_members("data/members.json", members)
            print(f"Участник добавлен с ID {new_member.id}: {new_member}")
            query = input_string(
                "Найти похожих по инструменту (Enter - пропустить): "
            )
            if query:
                show_members(find_member(members, query))
        elif choice == 0:
            save_bands("data/bands.json", bands)
            save_members("data/members.json", members)
            save_rehearsals("data/rehearsals.json", rehearsals)
            print("Данные сохранены. Выход.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
