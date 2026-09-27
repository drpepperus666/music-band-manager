# Система организации музыкальных групп (ПР3, ООП)

Консольное приложение для управления музыкальным коллективом:
учет групп, оценка кандидатов, планирование репетиций,
управление бронированиями.

## Целевая аудитория

Музыканты, лидеры и основатели музыкальных групп,
а также менеджеры начинающих музыкальных коллективов.

## Предметная область

Музыкальная индустрия, организация репетиционного процесса
и базовый менеджмент музыкальных коллективов.

## Основные класс

### Band — группа (`models/band.py`)

Представляет музыкальный коллектив (аналог `Room` из примера).

Атрибуты: `id`, `name`, `foundation_date`,
`required_instrument`, `is_active`, `members`.

Методы:

- `is_suitable_for(min_capacity)` — проверка вместимости;
- `validate_capacity()` — `@staticmethod` проверки корректности;
- `from_data()` — `@classmethod` создания из JSON;
- `to_dict()` — преобразование в JSON;
- `__str__()` — строковое представление.

### Member — участник (`models/member.py`)

Представляет участника/кандидата (аналог `User` из примера).

Атрибуты: `id`, `band` (ссылка на объект `Band`, не `band_id`),
`instrument`, `experience_years`, `status`.

Методы и свойства:

- `band_id` — `@property`, возвращает `band.id`;
- `from_data(data, bands)` — `@classmethod`, связывает с `Band`;
- `to_dict()` — сохраняет `band_id` вместо объекта;
- `__str__()` — строковое представление.

### Rehearsal — репетиция (`models/rehearsal.py`)

Бронирование группы на дату (аналог `Booking` из примера).

Атрибуты: `id`, `band` (ссылка на `Band`),
`rehearsal_date`, `participants`, `is_cancelled`.

Методы:

- `cancel()` — отмена без удаления из коллекции;
- `band_id` — `@property`;
- `from_data(data, bands)` / `to_dict()` — связь через `band_id`;
- `__str__()` — с учетом статуса (активна/отменена).

### Room — помещение (`models/room.py`, лайт-версия)

Вспомогательный класс для проверки студии,
без отдельного JSON-хранилища.

Атрибуты: `id`, `name`, `capacity`.
Методы: `is_suitable_for(band_size, has_large_equipment)`,
`validate_capacity()` (`@staticmethod`), `__str__`.

## Взаимодействие объектов

- `Member.band -> Band`, `Rehearsal.band -> Band`
- Доступ: `rehearsal.band.name`, `member.band.name`.
- Коллекции: `List[Band]`, `List[Member]`, `List[Rehearsal]`.
- Активная репетиция блокирует дату;
  отмененная (`is_cancelled=True`) — не блокирует.
- JSON хранит только `band_id`; объекты восстанавливаются
  в `storage.py` через поиск `find_band_by_id`.

## Возможности

- Просмотр и поиск групп (`find_band`, `sort_bands`).
- Проверка вместимости через метод (`Band.is_suitable_for`).
- Фильтрация активных (`filter_bands_by_active`,
  генератор `iter_active_bands`).
- Бронирование (`create_rehearsal`) и отмена
  (`cancel_rehearsal` -> `Rehearsal.cancel()`).
- Статистика (`get_bands_stats`).
- Оценка кандидата (`evaluate_candidate`).
- Участники: добавление с привязкой к объекту `Band`,
  поиск, сортировка, удаление, подсчет.
- Стоимость репетиции, проверка помещения (через `Room`).
- Сценарий `create_new_rehearsal()` в `main.py`:
  ввод ID -> поиск `Band` -> ввод даты ->
  проверка `is_band_available` -> создание `Rehearsal`.

## Структура проекта

- `main.py` — меню (15 пунктов + выход),
  `create_new_rehearsal()`, работа с `List[Band/Member/Rehearsal]`
- `models/__init__.py` — экспорт `Band, Member, Rehearsal, Room`
- `models/band.py` — класс `Band` + функции коллекций
- `models/member.py` — класс `Member` + функции коллекций
- `models/rehearsal.py` — класс `Rehearsal` + бронирование
- `models/room.py` — класс `Room` (лайт)
- `storage.py` — JSON <-> объекты (`with`,
  `FileNotFoundError`, `JSONDecodeError`)
- `utils.py` — ввод (`input_int`, `input_float`,
  `input_date`, `input_string`)
- `data/` — `bands.json`, `members.json`, `rehearsals.json`
  (репетиции хранят `is_cancelled`)
- `tests/` — 47 тестов: `test_bands.py`, `test_members.py`,
  `test_rehearsals.py`, `test_storage.py`, `test_room.py`
- `pytest.ini`, `requirements.txt`, `.flake8`

## Формат данных

`data/bands.json` — список групп (без изменений ПР2).

`data/members.json` — `band_id` для связи с группой.

`data/rehearsals.json` — связь через `band_id` + флаг:

```json
[
  {
    "id": 1,
    "band_id": 1,
    "rehearsal_date": "2026-09-15",
    "participants": 4,
    "is_cancelled": false
  }
]
```

## Требования

- Python 3.12+
- pytest, flake8, autopep8

Установка:

```text
pip install -r requirements.txt
```

Активация окружения `venv`:

```text
# WSL:
source venv/bin/activate
```

## Запуск программы

```text
python main.py
# через WSL:
wsl ./venv/bin/python main.py
```

## Запуск тестов

```text
pytest -v
# через WSL:
wsl ./venv/bin/pytest -v
```

Тесты проверяют: создание объектов и атрибуты, `__str__`,
методы (`is_suitable_for`, `cancel`), связь
`Rehearsal.band is Band`, правило «второе активное
бронирование запрещено, после отмены — разрешено»,
`from_data/to_dict`, коллекции, `storage` roundtrip.

## Проверка качества кода

```text
flake8 .
# через WSL:
wsl ./venv/bin/python -m flake8 .
```

## План развития

- веб-приложение;
- база данных;
- пользователи и API;
- контейнеризация;
- CI/CD.
