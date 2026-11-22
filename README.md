# Система организации музыкальных групп (ПР3 ООП + ПР5 Django + ПР6 шаблоны + ПР7 SQLite + ПР9 ORM + ПР10 Admin + ПР11 Forms)

Консольное приложение для управления музыкальным коллективом:
учет групп, оценка кандидатов, планирование репетиций,
управление бронированиями.

## Целевая аудитория

Музыканты, лидеры и основатели музыкальных групп,
а также менеджеры начинающих музыкальных коллективов.

## Предметная область

Музыкальная индустрия, организация репетиционного процесса
и базовый менеджмент музыкальных коллективов.

## Основные классы (консольный слой ПР3, сохранён без изменений)

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
  (репетиции хранят `is_cancelled`; консольный слой ПР3)
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
- `/rehearsals/` — список активных репетиций через форму
  `RehearsalFilterForm` (GET: дата/группа/поиск/сортировка,
  `cleaned_data` только после `is_valid()`),
  `annotate` + `F` + `values`, белый список сортировки,
  `Paginator` по 5, навигация с `{% querystring %}`;
  кнопки «Создать», «Редактировать», отмена через POST-форму
  (view-функция `rehearsal_list()`,
  шаблон `rehearsals/rehearsal_list.html`);
- `/rehearsals/create/` — создание репетиции (`RehearsalForm`,
  `initial` с текущей датой, проверка прошлого и занятости,
  `redirect` после сохранения);
- `/rehearsals/<int:rehearsal_id>/edit/` — редактирование
  (`instance=`, занятость без учёта себя через `exclude`);
- `/rehearsals/<int:rehearsal_id>/cancel/` — отмена только POST
  (`@require_POST`, `cancel()` → статус, без удаления;
  повторная отмена — 404, GET — 405);
- `/rehearsals/<int:rehearsal_id>/` — страница репетиции
  (`select_related("band")`, ссылка «Редактировать»);
- `/rehearsals/statistics/` — статистика по статусам
  и по группам (см. ПР10);
- `/bands/<slug:slug>/` — страница группы + загрузка фото
  (`BandImageForm`, `enctype="multipart/form-data"`,
  `request.FILES`, показ через `{{ band.image.url }}`);
- `/admin/` — админка (см. ПР10): добавлено поле фото группы.

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
  (`homepage:index`, `bands:list`,
  `rehearsals:list`, `rehearsals:statistics`);
  ссылки на деталки — в карточках через `get_absolute_url`;
- пространства имен: `app_name` в `homepage/urls.py`,
  `bands/urls.py`, `rehearsals/urls.py`;
- карточка группы `bands/includes/band_card.html`,
  статус репетиции `rehearsals/includes/rehearsal_status.html`
  подключены через `{% include %}`;
- списки — цикл `{% for %}` с `{% empty %}`,
  состояния — `{% if %}` (`is_active`, `status`,
  `available`, наличие объекта);
- фильтры: `{{ bands|length }}`, `{{ page_obj.paginator.count }}`,
  `{{ band.name|default:"Без названия" }}`;
- статика `homepage/static/homepage/`: `css/style.css`
  (стили `.band-card`, `.rehearsal-status`, `.bandly-logo`),
  `js/main.js` (текущий год в подвале), `img/logo.png`;
  подключение через `{% load static %}` и `{% static %}`.

## Структура Django-проекта (ПР5–ПР10)

```text
.
├── manage.py
├── bandly/            # конфигурация Django-проекта
│   ├── settings.py    # ru-RU, Europe/Moscow, DIRS templates/
│   │                   # + toolbar, INTERNAL_IPS, band_context (ПР10)
│   ├── urls.py        # include() приложений + handler404 + __debug__/
│   ├── asgi.py
│   └── wsgi.py
├── templates/         # base.html + includes/navigation.html (ПР6)
├── bands/             # группы (ПР9 модель, ПР10 admin/slug, ПР11 фото)
│   ├── models.py      # Band: + slug, get_absolute_url(), save(), image
│   ├── context_processors.py  # band_context (ПР10)
│   ├── forms.py       # BandImageForm (ПР11)
│   ├── admin.py       # BandAdmin + MemberInline/RehearsalInline
│   ├── views.py       # на ORM + status + slug-деталка + фото (ПР11)
│   ├── urls.py        # list/detail(slug)/available
│   ├── migrations/    # 0001 (ПР9), 0002–0004 slug (ПР10), 0005 image
│   └── templates/bands/
├── members/           # участники (ПР9 модель, ПР10 admin/GeneratedField)
│   ├── models.py      # Member: + is_experienced (GeneratedField)
│   ├── admin.py       # MemberAdmin
│   └── migrations/    # 0001 (ПР9), 0002 is_experienced
├── rehearsals/        # репетиции (формы ПР11, статусы ПР10)
│   ├── models.py      # Rehearsal: status TextChoices + QuerySet/Manager
│   ├── forms.py       # RehearsalFilterForm + RehearsalForm (ПР11)
│   ├── admin.py       # RehearsalAdmin (действия, inline-поля)
│   ├── views.py       # CRUD через формы + ORM (ПР11)
│   ├── urls.py        # list/create/statistics/edit/cancel/detail
│   ├── migrations/    # 0001 (ПР9), 0002–0004 статусы (ПР10)
│   └── templates/rehearsals/  # + rehearsal_form.html (ПР11)
├── models/            # классы ПР3 (консольный слой, без изменений)
├── db/                # SQLite-слой ПР7 + import_sqlite_to_orm.py (ПР9/10)
├── sql/               # schema.sql, queries.sql (ПР7, исторический слой)
├── data/              # JSON ПР3 + bands.sqlite (ПР7, источник переноса)
└── tests/             # 47 тестов ПР3 (консольный слой)
```

Примечание: флаг `is_cancelled` остался только в исторических слоях
(консольные классы `models/`, `sql/schema.sql`, `tests/`, `data/`);
в Django ORM его заменил `Rehearsal.status`.

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
- `Rehearsal` (`rehearsals/models.py`, с ПР10 — `status` вместо флага):
  `band = ForeignKey(Band, PROTECT, related_name="rehearsals")`,
  `rehearsal_date` (`DateField`), `participants`,
  `status` (`TextChoices`: `active/cancelled/completed`);
  метод `cancel()` (перевод в `cancelled` + `save(update_fields=...)`).

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
- `db.sqlite3` закоммичена осознанно: демо-данные, миграции
  и учётные записи админки нужны для защиты без перенастройки
  (новые `*.sqlite3` в `.gitignore`).

## Формы Django (ПР11)

- `RehearsalFilterForm` (`rehearsals/forms.py`, `forms.Form`):
  `date`/`band` (`ModelChoiceField`)/`q`/`sort` (`ChoiceField`),
  всё `required=False`; форма связана через
  `RehearsalFilterForm(request.GET or None)`, значения — только из
  `cleaned_data` после `is_valid()`; невалидный ввод — сообщение
  «Проверьте корректность параметров фильтрации» + ошибки полей,
  фильтрация не применяется;
- `RehearsalForm` (`forms.ModelForm`, `fields = ["band",
  "rehearsal_date", "participants"]`, `labels`/`help_texts`/виджеты
  Bootstrap): `clean_rehearsal_date()` запрещает прошлое
  (`timezone.localdate()`), `clean()` запрещает дубль активной
  репетиции (`exists()`, при редактировании — `exclude(pk=...)`);
  статус задаёт сервер (`default=active`), в форме его нет;
- представления: `rehearsal_create` (GET — пустая + `initial`,
  POST — проверка → `save()` → `redirect`), `rehearsal_update`
  (`instance=`), `rehearsal_cancel` (`@require_POST`,
  только active, `cancel()`, повтор — 404);
- шаблоны: общий `rehearsal_form.html` (create/update:
  `{% csrf_token %}`, цикл полей, `field.errors`,
  `form.non_field_errors`), кнопки в списке и деталке;
- фото группы: `Band.image` (`ImageField`, `upload_to="bands/"`,
  миграция `0005`, `Pillow`), `MEDIA_URL`/`MEDIA_ROOT` + `static()`
  при `DEBUG` (`media/` в `.gitignore`), `BandImageForm` на странице
  группы (`request.FILES`, показ `{{ band.image.url }}`), поле
  доступно и в админке.

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

Django-тесты форм и представлений (`rehearsals/tests.py`,
17 тестов: фильтр, валидация даты/занятости/участников,
создание/редактирование/отмена, менеджер):

```text
wsl ./venv/bin/python manage.py test rehearsals
```

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

## Текущее состояние и план развития (ПР11)

Реализовано (ПР5–ПР11):

- Django-проект `bandly`, приложения
  (`homepage`, `bands`, `members`, `rehearsals`);
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
- динамические URL `<slug:slug>` (группы), `<int:rehearsal_id>`;
- обработка 404 (`get_object_or_404` + `handler404`);
- консольное приложение ПР3 сохранено без изменений;
- слой SQLite ПР7 сохранён как исторический (`sql/`, `db/database.py`);
- слой Django ORM (ПР9): модели, миграции, перенос данных,
  фильтры/сортировка/пагинация в представлениях;
- административная панель (ПР10): три `ModelAdmin`, inline,
  действия, локализация; статусы `TextChoices` + менеджер;
  `GeneratedField`, `slug` + `get_absolute_url`, контекстный
  процессор, Debug Toolbar;
- формы Django (ПР11): фильтр через `Form`, создание/редактирование
  через `ModelForm`, отмена через POST, фото через `ImageField`.

Планируется (далее):

- пользователи и API;
- контейнеризация;
- CI/CD.
