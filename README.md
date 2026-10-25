# Система организации музыкальных групп (ПР3 ООП + ПР5 Django)

Консольное приложение для управления музыкальным коллективом:
учет групп, оценка кандидатов, планирование репетиций,
управление бронированиями.

## Целевая аудитория

Музыканты, лидеры и основатели музыкальных групп,
а также менеджеры начинающих музыкальных коллективов.

## Предметная область

Музыкальная индустрия, организация репетиционного процесса
и базовый менеджмент музыкальных коллективов.

## Основные классы

### Band — группа (`models/band.py`)

Представляет музыкальный коллектив.

Атрибуты: `id`, `name`, `foundation_date`,
`required_instrument`, `is_active`, `members`.

Методы:

- `is_suitable_for(min_capacity)` — проверка вместимости;
- `validate_capacity()` — `@staticmethod` проверки корректности;
- `from_data()` — `@classmethod` создания из JSON;
- `to_dict()` — преобразование в JSON;
- `__str__()` — строковое представление.

### Member — участник (`models/member.py`)

Представляет участника/кандидата.

Атрибуты: `id`, `band` (ссылка на объект `Band`, не `band_id`),
`instrument`, `experience_years`, `status`.

Методы и свойства:

- `band_id` — `@property`, возвращает `band.id`;
- `from_data(data, bands)` — `@classmethod`, связывает с `Band`;
- `to_dict()` — сохраняет `band_id` вместо объекта;
- `__str__()` — строковое представление.

### Rehearsal — репетиция (`models/rehearsal.py`)

Бронирование группы на дату.

Атрибуты: `id`, `band` (ссылка на `Band`),
`rehearsal_date`, `participants`, `is_cancelled`.

Методы:

- `cancel()` — отмена без удаления из коллекции;
- `band_id` — `@property`;
- `from_data(data, bands)` / `to_dict()` — связь через `band_id`;
- `__str__()` — с учетом статуса (активна/отменена).

### Room — помещение

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

`data/bands.json` — список групп.

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
- Django 5.2, pytest, flake8, autopep8

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

Консольная версия (сохранена с ПР3):

```text
python main.py
# через WSL:
wsl ./venv/bin/python main.py
```

Веб-версия (Django, ПР5):

```text
wsl ./venv/bin/python manage.py migrate
wsl ./venv/bin/python manage.py runserver
```

После запуска открыть в браузере:

```text
http://127.0.0.1:8000/
```

## Страницы веб-интерфейса (ПР5)

- `/` — главная страница: описание приложения и навигация
  (view-функция `index()`);
- `/bands/` — список групп: объекты `Band` из `data/bands.json`
  (view-функция `bands()`);
- `/bands/<int:band_id>/` — страница группы, доступность на текущую
  дату через `is_band_available()` (view-функция `band_detail()`);
- `/rehearsals/` — список репетиций: объекты `Rehearsal`
  из `data/rehearsals.json` (view-функция `rehearsals()`);
- `/rehearsals/<int:rehearsal_id>/` — страница репетиции
  (view-функция `rehearsal_detail()`).

Если группа или репетиция с указанным идентификатором не найдена,
страница возвращает код статуса 404. Несуществующие адреса
обрабатывает `handler404` (`homepage.views.page_not_found`).

## Структура Django-проекта (ПР5)

```text
.
├── manage.py
├── bandly/            # конфигурация Django-проекта
│   ├── settings.py    # LANGUAGE_CODE ru-RU, TIME_ZONE Europe/Moscow
│   ├── urls.py        # include() трех приложений + handler404
│   ├── asgi.py
│   └── wsgi.py
├── homepage/          # главная страница + page()
│   ├── views.py       # page(), index(), page_not_found()
│   └── urls.py
├── bands/             # группы
│   ├── views.py       # bands(), band_detail()
│   └── urls.py
├── rehearsals/        # репетиции
│   ├── views.py       # rehearsals(), rehearsal_detail()
│   └── urls.py
├── models/            # классы ПР3 (Band, Member, Rehearsal, Room)
├── data/              # bands.json, members.json, rehearsals.json
└── tests/             # 47 тестов ПР3
```

HTML формируется в Python через вспомогательную функцию `page()`
в `homepage/views.py`: единый каркас (кодировка, viewport,
Bootstrap 5.3 через CDN, навигация, `container`). В следующей работе
каркас переедет в базовый шаблон, `page()` будет удалена.

## Запуск тестов

```text
pytest -v
# через WSL:
wsl ./venv/bin/python -m pytest -v
```

Тесты проверяют: создание объектов и атрибуты, `__str__`,
методы (`is_suitable_for`, `cancel`), связь
`Rehearsal.band is Band`, правило «второе активное
бронирование запрещено, после отмены — разрешено»,
`from_data/to_dict`, коллекции, `storage` roundtrip.

Системная проверка Django:

```text
wsl ./venv/bin/python manage.py check
```

## Проверка качества кода

```text
flake8 .
# через WSL:
wsl ./venv/bin/python -m flake8 .
```

## Git

```text
git status
git add .
git commit -m "PR5: add Django project and web pages"
```

## Текущее состояние и план развития (ПР5)

Реализовано:

- Django-проект `bandly` и три приложения
  (`homepage`, `bands`, `rehearsals`);
- маршрутизация URL двух уровней (`include()`);
- view-функции и страницы (главная, списки, детальные);
- динамические URL `<int:band_id>`, `<int:rehearsal_id>`;
- обработка 404 (ветка «не найдено» + `handler404`);
- отображение данных предметной области из JSON через логику ПР3
  (`load_bands`, `find_band_by_id`, `is_band_available`,
  `find_rehearsal_by_id`, подсчет участников);
- навигация между страницами;
- оформление Bootstrap 5.3.

Планируется:

- переход на Django-шаблоны и отказ от функции `page()`;
- база данных SQLite и SQL-запросы;
- перенос сущностей в Django ORM;
- формы создания и редактирования;
- пользователи и API;
- контейнеризация;
- CI/CD.
