"""Перенос данных ПР7 (data/bands.sqlite) в таблицы Django ORM (ПР9).

Исходная база сохраняется без изменений, целевая база Django
заполняется через ORM с сохранением идентификаторов и связей.
Порядок: сначала независимые сущности (группы), затем зависимые
(участники, репетиции).

Запуск из корня проекта:
    python db/import_sqlite_to_orm.py
"""

import os
import sqlite3
import sys
from datetime import date
from pathlib import Path

import django
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
SOURCE_DB = BASE_DIR / "data" / "bands.sqlite"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bandly.settings")
django.setup()

from bands.models import Band  # noqa: E402
from members.models import Member  # noqa: E402
from rehearsals.models import Rehearsal  # noqa: E402


def main():
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Исходная база не найдена: {SOURCE_DB}")
    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row
        bands = connection.execute(
            """
SELECT id, name, foundation_date, required_instrument, is_active
FROM bands
ORDER BY id
"""
        ).fetchall()
        members = connection.execute(
            """
SELECT id, band_id, instrument, experience_years, status
FROM members
ORDER BY id
"""
        ).fetchall()
        rehearsals = connection.execute(
            """
SELECT id, band_id, rehearsal_date, participants, is_cancelled
FROM rehearsals
ORDER BY id
"""
        ).fetchall()
        with transaction.atomic():
            for row in bands:
                Band.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "name": row["name"],
                        "foundation_date": date.fromisoformat(
                            row["foundation_date"]
                        ),
                        "required_instrument": row["required_instrument"],
                        "is_active": bool(row["is_active"]),
                    },
                )
            for row in members:
                Member.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "band_id": row["band_id"],
                        "instrument": row["instrument"],
                        "experience_years": row["experience_years"],
                        "status": row["status"],
                    },
                )
            for row in rehearsals:
                Rehearsal.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "band_id": row["band_id"],
                        "rehearsal_date": date.fromisoformat(
                            row["rehearsal_date"]
                        ),
                        "participants": row["participants"],
                        "is_cancelled": bool(row["is_cancelled"]),
                    },
                )
    print("Перенос данных завершён.")
    print(f"Групп: {Band.objects.count()}")
    print(f"Участников: {Member.objects.count()}")
    print(f"Репетиций: {Rehearsal.objects.count()}")


if __name__ == "__main__":
    main()
