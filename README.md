# Система организации музыкальных групп

Консольное приложение для управления музыкальным коллективом: учет групп, оценка кандидатов, планирование репетиций, управление бронированиями.

## Целевая аудитория
Музыканты, лидеры и основатели музыкальных групп, а также менеджеры начинающих музыкальных коллективов.

## Предметная область
Музыкальная индустрия, организация репетиционного процесса и базовый менеджмент музыкальных коллективов.

## Основные сущности
- Группа (Band)
- Участник/Кандидат (Member)
- Репетиция (Rehearsal)

## Возможности (ПР2)
- Просмотр и поиск групп по названию (`find_band`).
- Проверка вместимости группы по числу участников (`check_band_capacity`).
- Сортировка групп по названию (`sort_bands`, `lambda`).
- Фильтрация активных групп (`filter_bands_by_active`, генератор `iter_active_bands`).
- Проверка доступности группы на дату (`is_band_available` + `get_rehearsal_status` из ПР1).
- Бронирование (`add_rehearsal`) и отмена (`cancel_rehearsal`) репетиций.
- Статистика: всего групп/активных/репетиций, среднее число участников (`get_bands_stats`).
- Оценка кандидата (`evaluate_candidate` из ПР1, модуль `members`).
- Добавление / поиск / сортировка / удаление участников (`members.py`, `lambda`, генератор).
- Расчет стоимости репетиции (`calculate_rehearsal_cost` из ПР1).
- Проверка помещения (`check_room_suitability` из ПР1).
- Статус группы (`get_band_status` из ПР1).

## Структура проекта
- `main.py` — точка запуска приложения и меню (15 пунктов + выход)
- `bands.py` — функции управления группами (добавление, поиск, фильтрация, сортировка, генератор, статистика)
- `members.py` — функции управления участниками (сущность Member: добавление, поиск, фильтр по `band_id`, сортировка `lambda`, генератор, удаление, оценка кандидата из ПР1)
- `rehearsals.py` — функции управления репетициями (бронирование, отмена, проверка доступности)
- `storage.py` — загрузка и сохранение данных в JSON-файлах (`with`, обработка `FileNotFoundError`, `JSONDecodeError`)
- `utils.py` — вспомогательные функции ввода (`input_int`, `input_float`, `input_date`, `input_string`) с обработкой ошибок
- `data/` — JSON-файлы данных (`bands.json`, `members.json`, `rehearsals.json`)
- `tests/` — автоматизированные тесты (`test_bands.py`, `test_members.py`, `test_rehearsals.py`, `test_storage.py`), 28 тестов
- `README.md` — документация проекта
- `requirements.txt` — зависимости проекта (`pytest`, `flake8`, `autopep8`)
- `pytest.ini` — настройки `pytest` (`pythonpath=.`, `testpaths=tests`)

## Формат данных

`data/bands.json` — список групп:
```json
[
  {
    "id": 1,
    "name": "Nirvana",
    "foundation_date": "2026-06-06",
    "required_instrument": "Бас-гитара",
    "is_active": true,
    "members": ["Курт Кобейн", "Крист Новоселич", "Дэйв Грол"]
  }
]
```

`data/rehearsals.json` — список репетиций:
```json
[
  {
    "id": 1,
    "band_id": 1,
    "rehearsal_date": "2026-09-15",
    "participants": 4
  }
]
```

`data/members.json` — список кандидатов:
```json
[
  {
    "id": 1,
    "band_id": 1,
    "instrument": "Бас-гитара",
    "experience_years": 3,
    "status": "Одобрено: Приглашаем на прослушивание!"
  }
]
```

## Связи сущностей
- `Member.band_id -> Band.id`: много участников к одной группе (`filter_members_by_band`, `count_members_for_band` в `members.py`).
- `Rehearsal.band_id -> Band.id`: много репетиций к одной группе (`is_band_available`, `add_rehearsal` в `rehearsals.py`).
- `Band + Rehearsal`: совместная статистика (`get_bands_stats` в `bands.py`).

## Требования
- Python 3.12+
- pytest
- flake8
- autopep8

Установка зависимостей:
```
pip install -r requirements.txt
```
Примечание: виртуальное окружение `venv/` создано в WSL (Linux), поэтому команды запуска выполняются через WSL (`wsl ./venv/bin/...`).

## Запуск программы
```
python main.py
# через WSL:
source venv/bin/activate
./venv/bin/python main.py
```

## Запуск тестов
```
pytest
# через WSL:
./venv/bin/pytest -v
```

## Проверка качества кода
```
flake8
# через WSL:
./venv/bin/flake8
```

## Проверка форматирования (autopep8)
```
autopep8 --version
autopep8 --diff --recursive .
# только проверка, без изменений
# через WSL:
./venv/bin/autopep8 --version
./venv/bin/autopep8 --diff --recursive .
# автоисправление:
./venv/bin/autopep8 --in-place --recursive bands.py members.py rehearsals.py storage.py utils.py main.py
```

## План развития
На следующих этапах планируется:
- разработка веб-приложения;
- подключение базы данных;
- реализация пользователей;
- разработка API;
- контейнеризация приложения;
- настройка CI/CD;
- переход на ООП (ПР3).