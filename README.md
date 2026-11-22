# Система организации музыкальных групп (ПР3 ООП + ПР5 Django + ПР6 шаблоны + ПР7 SQLite + ПР9 ORM + ПР10 Admin)

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

## Страницы веб-интерфейса (ПР5–ПР9)

- `/` — главная страница: описание приложения и навигация
  (view-функция `index()`, шаблон `homepage/index.html`);
- `/bands/` — список групп через ORM (`order_by("name")`)
  + поиск по названию/инструменту (`Q`, `icontains`)
  (view-функция `band_list()`, шаблон `bands/band_list.html`);
- `/bands/<slug:slug>/` — страница группы через ORM
  (`get_object_or_404(Band, slug=slug)`, `members.count()`,
  доступность на текущую дату через `active().exists()`)
  (view-функция `band_detail()`, шаблон `bands/band_detail.html`);
- `/bands/available/?date=YYYY-MM-DD` — поиск свободных групп
  на дату, форма GET + `active()` и `exclude(pk__in=...)`
  (отменённые/завершённые не блокируют дату)
  (view-функция `available_bands()`,
  шаблон `bands/available.html`);
- `/rehearsals/` — список активных репетиций через ORM
  (`Rehearsal.objects.active()`, `annotate` + `F` + `values`,
  фильтры по дате/группе, поиск, сортировка из белого списка,
  `Paginator` по 5, навигация с `{% querystring %}`)
  (view-функция `rehearsal_list()`,
  шаблон `rehearsals/rehearsal_list.html`);
- `/rehearsals/<int:rehearsal_id>/` — страница репетиции
  (`select_related("band")`, шаблон обращается
  к `rehearsal.band.name` и статусу через общий include)
  (view-функция `rehearsal_detail()`,
  шаблон `rehearsals/rehearsal_detail.html`);
- `/rehearsals/statistics/` — статистика: число активных репетиций
  по группам (`Count` + `Q(status=...)`) и сводные итоги
  (`total/active/cancelled/completed` через `aggregate`,
  средний состав через `Avg`)
  (view-функция `statistics()`,
  шаблон `rehearsals/statistics.html`).
- `/admin/` — административная панель: группы, участники,
  репетиции (списки, поиск, фильтры, сортировка, inline,
  массовые действия, Debug Toolbar на страницах сайта).

Несуществующие объекты обрабатывает `get_object_or_404`
(ответ 404). Несуществующие адреса
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

## Структура Django-проекта (ПР5–ПР9)

```text
.
├── manage.py
├── bandly/            # конфигурация Django-проекта
│   ├── settings.py    # ru-RU, Europe/Moscow, DIRS templates/
│   ├── urls.py        # include() приложений + handler404
│   ├── asgi.py
│   └── wsgi.py
├── templates/         # base.html + includes/navigation.html (ПР6)
├── homepage/          # главная страница
│   ├── views.py       # index(), page_not_found() через render()
│   ├── urls.py        # app_name homepage, name index
│   ├── templates/homepage/  # index.html, 404.html
│   └── static/homepage/     # css/style.css, js/main.js, img/logo.png
├── bands/             # группы (ПР9: модель Band)
│   ├── models.py      # Band: name, foundation_date,
│   │                   # required_instrument, is_active
│   ├── views.py       # band_list/detail(), available_bands() на ORM
│   ├── urls.py        # app_name bands, names list/detail/available
│   ├── migrations/    # 0001_initial (ПР9)
│   └── templates/bands/     # band_list/detail/available
│       └── includes/band_card.html
├── members/           # участники (ПР9: модель Member)
│   ├── models.py      # Member: band FK(CASCADE), instrument,
│   │                   # experience_years, status
│   └── migrations/    # 0001_initial (ПР9)
├── rehearsals/        # репетиции (ПР9: модель Rehearsal)
│   ├── models.py      # Rehearsal: band FK(PROTECT), rehearsal_date,
│   │                   # participants, is_cancelled + cancel()
│   ├── views.py       # rehearsal_list/detail(), statistics() на ORM
│   ├── urls.py        # app_name rehearsals, names list/detail/statistics
│   ├── migrations/    # 0001_initial (ПР9)
│   └── templates/rehearsals/  # list/detail/statistics
│       └── includes/rehearsal_status.html
├── models/            # классы ПР3 (Band, Member, Rehearsal, Room)
├── db/                # SQLite-слой ПР7 + import_sqlite_to_orm.py (ПР9)
├── sql/               # schema.sql, queries.sql (12 запросов) (ПР7)
├── data/              # JSON ПР3 + bands.sqlite (ПР7, источник переноса)
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

## Слой Django ORM (ПР9)

Представления больше не используют `sqlite3` напрямую:
данные идут по цепочке
представление → Django ORM → SQLite → объекты моделей.
Файлы `sql/` и `db/database.py` сохранены как реализация ПР7,
источником переноса служит `data/bands.sqlite`,
рабочая база Django — `db.sqlite3` (`DATABASES` не менялась).

Модели (`Meta.ordering`, русская `verbose_name`, `__str__`):

- `Band` (`bands/models.py`): `name`, `foundation_date`
  (`DateField`), `required_instrument`, `is_active`;
- `Member` (`members/models.py`): `band = ForeignKey(Band,
  CASCADE, related_name="members")`, `instrument`,
  `experience_years`, `status`;
- `Rehearsal` (`rehearsals/models.py`): `band = ForeignKey(Band,
  PROTECT, related_name="rehearsals")`, `rehearsal_date`
  (`DateField`), `participants`, `is_cancelled`;
  метод `cancel()` (флаг + `save(update_fields=...)`).

Порядок работы с нуля:

```text
python manage.py makemigrations bands members rehearsals
python manage.py migrate
python db/import_sqlite_to_orm.py
python manage.py runserver
```

Скрипт `db/import_sqlite_to_orm.py` читает `data/bands.sqlite`
и переносит записи через `update_or_create` с сохранением `id`
(группы → участники → репетиции, одна транзакция
`transaction.atomic()`, строки дат — через `date.fromisoformat`,
флаги `0/1` — в `bool`). Проверка: 2 группы, 1 участник,
1 репетиция; `Rehearsal.objects.select_related("band")`
возвращает связанную группу.

Ключевые ORM-приемы во views (всего >15 выражений):
`all/order_by`, `get_object_or_404`, `filter` (в т.ч. по `band_id`
и `band__name`), `exclude(pk__in=...)`, `Q` + `icontains` (поиск),
белый список полей для `order_by` (сортировка), `annotate` + `F`
+ `values` / `values_list`, `select_related`, `count`,
`aggregate(Avg)`, `annotate(Count(..., filter=Q(...)))`,
`Paginator.get_page` + `{% querystring %}` (пагинация по 5
с сохранением фильтров).

## Административная панель и развитие ORM (ПР10)

Суперпользователь: `python manage.py createsuperuser`
(вход — `/admin/`). Тестовая группа «Bandly Operators»
(просмотр/создание/изменение групп без удаления) и пользователь
`operator` созданы для проверки разрешений.

- `BandAdmin`: столбцы (`rehearsals_count` через `annotate` +
  `Count(filter=Q(status=...))`, `site_link` через
  `get_absolute_url`), поиск, фильтр `is_active`, сортировка,
  `list_editable = ("is_active",)`, `readonly_fields = ("id",)`,
  inline участников и репетиций, `view_on_site`;
- `MemberAdmin`: столбцы (включая вычисляемое `is_experienced`),
  поиск по инструменту/статусу/группе, фильтр, `list_editable`
  для стажа, сортировка по стажу;
- `RehearsalAdmin`: столбец инструмента группы (`ordering`
  по связанному полю), поиск `band__name`, фильтры дата/статус,
  `list_select_related = ("band",)`, `date_hierarchy`,
  `autocomplete_fields`, действия «Отменить»/«Вернуть в активные».
- Русская локализация: `AppConfig.verbose_name` («Группы»,
  «Участники», «Репетиции»), `verbose_name` моделей и полей,
  `help_text` у подсказок.

Развитие моделей:

- `Rehearsal.status` — `TextChoices` (`active/cancelled/completed`)
  вместо `is_cancelled` (удалён миграцией `0004`);
  перенос значений — миграция данных `0003_migrate_statuses`;
  метод `cancel()` переводит в `cancelled`;
- `RehearsalQuerySet`/`RehearsalManager`: `active()`, `cancelled()`,
  `completed()`, `for_date()`; представления используют
  `Rehearsal.objects.active()`;
- `Member.is_experienced` — `GeneratedField` (`experience_years >= 3`,
  `db_persist=True`), пересчёт на стороне базы;
- `Band.slug` — `SlugField(unique)` из транслитерации названия + `pk`
  (`Unidecode` + `slugify`, миграция данных `0003_populate_slugs`,
  автосоздание в `save()`); деталка — `<slug:slug>/`,
  ссылки — `{{ band.get_absolute_url }}`;
- контекстный процессор `bands.context_processors.band_context`
  (`site_name`, `bands_count`) — счётчик групп в навигации;
- Django Debug Toolbar (`debug_toolbar`, `INTERNAL_IPS`,
  маршрут `__debug__/` при `DEBUG`): вкладка SQL подтверждает
  один запрос списка (`annotate` + `F` + `values`) и JOIN
  в деталке (`select_related`).

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
