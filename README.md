# Система организации музыкальных групп (ПР3 ООП + ПР5 Django + ПР6 шаблоны + ПР7 SQLite)

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

## Страницы веб-интерфейса (ПР5–ПР7)

- `/` — главная страница: описание приложения и навигация
  (view-функция `index()`, шаблон `homepage/index.html`);
- `/bands/` — список групп из SQLite
  (view-функция `band_list()`, шаблон `bands/band_list.html`);
- `/bands/<int:band_id>/` — страница группы из SQLite, доступность
  на текущую дату SQL-запросом
  (view-функция `band_detail()`, шаблон `bands/band_detail.html`);
- `/bands/available/?date=YYYY-MM-DD` — поиск свободных групп
  на дату, форма GET + параметризованный запрос с `NOT IN`
  (view-функция `available_bands()`,
  шаблон `bands/available.html`);
- `/rehearsals/` — список активных репетиций из SQLite (`JOIN`)
  (view-функция `rehearsal_list()`,
  шаблон `rehearsals/rehearsal_list.html`);
- `/rehearsals/<int:rehearsal_id>/` — страница репетиции из SQLite
  (view-функция `rehearsal_detail()`,
  шаблон `rehearsals/rehearsal_detail.html`);
- `/rehearsals/statistics/` — статистика: число репетиций
  по группам (`LEFT JOIN` + `GROUP BY`)
  (view-функция `statistics()`,
  шаблон `rehearsals/statistics.html`).

Если группа или репетиция с указанным идентификатором не найдена,
страница возвращает код статуса 404. Несуществующие адреса
обрабатывает `handler404` (`homepage.views.page_not_found`,
шаблон `homepage/404.html`).

## Django-шаблоны (ПР6)

HTML вынесен из Python-кода в шаблоны, функция `page()` удалена,
представления используют `render(request, template, context)`:

- базовый шаблон `templates/base.html`: структура документа,
  Bootstrap 5.3 через CDN, собственный CSS, логотип, навигация,
  блоки `title`/`content`, подвал с годом через `main.js`;
- навигация `templates/includes/navigation.html` подключена через
  `{% include %}`, ссылки через `{% url %}`
  (`homepage:index`, `bands:list`, `bands:detail`, `bands:available`,
  `rehearsals:list`, `rehearsals:detail`, `rehearsals:statistics`);
- пространства имен: `app_name` в `homepage/urls.py`,
  `bands/urls.py`, `rehearsals/urls.py`;
- карточка группы `bands/includes/band_card.html`,
  статус репетиции `rehearsals/includes/rehearsal_status.html`
  подключены через `{% include %}`;
- списки — цикл `{% for %}` с `{% empty %}`,
  состояния — `{% if %}` (`is_active`, `is_cancelled`,
  `available`, наличие объекта);
- фильтры: `{{ bands|length }}`, `{{ rehearsals|length }}`,
  `{{ band.name|default:"Без названия" }}`;
- статика `homepage/static/homepage/`: `css/style.css`
  (стили `.band-card`, `.rehearsal-status`, `.bandly-logo`),
  `js/main.js` (текущий год в подвале), `img/logo.png`;
  подключение через `{% load static %}` и `{% static %}`.

## Структура Django-проекта (ПР5–ПР7)

```text
.
├── manage.py
├── bandly/            # конфигурация Django-проекта
│   ├── settings.py    # ru-RU, Europe/Moscow, DIRS templates/
│   ├── urls.py        # include() трех приложений + handler404
│   ├── asgi.py
│   └── wsgi.py
├── templates/         # base.html + includes/navigation.html (ПР6)
├── homepage/          # главная страница
│   ├── views.py       # index(), page_not_found() через render()
│   ├── urls.py        # app_name homepage, name index
│   ├── templates/homepage/  # index.html, 404.html
│   └── static/homepage/     # css/style.css, js/main.js, img/logo.png
├── bands/             # группы
│   ├── views.py       # band_list(), band_detail(), available_bands()
│   ├── urls.py        # app_name bands, names list/detail/available
│   └── templates/bands/     # band_list/detail/available
│       └── includes/band_card.html
├── rehearsals/        # репетиции
│   ├── views.py       # rehearsal_list/detail(), statistics()
│   ├── urls.py        # app_name rehearsals, names list/detail/statistics
│   └── templates/rehearsals/  # list/detail/statistics
│       └── includes/rehearsal_status.html
├── models/            # классы ПР3 (Band, Member, Rehearsal, Room)
├── db/                # SQLite-слой ПР7: database.py, import_json.py
├── sql/               # schema.sql, queries.sql (12 запросов) (ПР7)
├── data/              # JSON ПР3 + bands.sqlite (ПР7)
└── tests/             # 47 тестов ПР3
```

Генерация HTML через функцию `page()` (ПР5) удалена в ПР6:
представления готовят контекст и вызывают `render()`,
разметка хранится в шаблонах.

## База данных SQLite (ПР7)

Файл `data/bands.sqlite` создается из JSON:

```text
wsl ./venv/bin/python -m db.import_json
```

Схема `sql/schema.sql`:

- `bands(id, name, foundation_date, required_instrument, is_active)`
  — `id INTEGER PRIMARY KEY`, флаги хранятся как `0/1`;
- `members(id, band_id, instrument, experience_years, status)` —
  `band_id FOREIGN KEY REFERENCES bands(id)`;
- `rehearsals(id, band_id, rehearsal_date, participants,
  is_cancelled)` — `band_id FOREIGN KEY REFERENCES bands(id)`,
  дата строкой `YYYY-MM-DD`, отмена флагом `0/1`.

Подключение `db/database.py`: `get_connection()` —
`sqlite3.connect`, `PRAGMA foreign_keys = ON`,
`row_factory = sqlite3.Row` (доступ к полям по именам
в Python и в шаблонах). Импорт `db/import_json.py`:
`executemany()`, параметры `?`, `commit()`/`rollback()`.

Файл `sql/queries.sql` — 12 проверенных запросов (все виды
представлены минимум дважды): списки (`ORDER BY`),
фильтрация (`WHERE`, `LIKE`), соединения (`JOIN`, `LEFT JOIN`),
агрегаты (`COUNT`, `AVG`), группировки (`GROUP BY`),
фильтрация групп (`HAVING`), подзапрос свободных групп
(`NOT IN`). Значения передаются только параметрами `?`,
конкатенация строк и f-строки для SQL запрещены.

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
git commit -m "PR7: add SQLite database and SQL queries"
```

## Текущее состояние и план развития (ПР7)

Реализовано:

- Django-проект `bandly` и три приложения
  (`homepage`, `bands`, `rehearsals`);
- маршрутизация URL двух уровней (`include()`),
  именованные маршруты и пространства имен;
- view-функции через `render()` и страницы-шаблоны
  (главная, списки, детальные, 404);
- базовый шаблон `base.html` (`extends`/`block`),
  включаемые шаблоны (`include`: навигация, карточка группы,
  статус репетиции);
- контекст, циклы `{% for %}` с `{% empty %}`, условия `{% if %}`;
- фильтры `length`, `default`;
- собственные статические файлы (CSS, JS, логотип) + Bootstrap 5.3;
- динамические URL `<int:band_id>`, `<int:rehearsal_id>`;
- обработка 404 (ветка «не найдено» + `handler404`);
- консольное приложение ПР3 сохранено: логика
  (`load_bands`, `find_band_by_id`, `is_band_available`,
  `find_rehearsal_by_id`, подсчет участников) работает в `main.py`;
  веб-слой получает данные из SQLite через `get_connection()`;
- навигация между страницами через `{% url %}`
  (Главная, Группы, Репетиции, Статистика);
- слой SQLite: `data/bands.sqlite`, `sql/schema.sql`,
  `db/database.py`, `db/import_json.py`, 12 запросов
  в `sql/queries.sql` (списки, `WHERE`, `JOIN`, `COUNT`/`AVG`,
  `GROUP BY`, `HAVING`, подзапрос `NOT IN`);
- страницы на данных из SQLite: список групп, список репетиций,
  поиск свободных групп по дате (параметризованный запрос),
  статистика по группам; `sqlite3.Row` + `context` + шаблоны.

Планируется:

- перенос сущностей в Django ORM;
- формы создания и редактирования;
- пользователи и API;
- контейнеризация;
- CI/CD.
