"""Страницы групп: данные из SQLite (ПР7)."""

from datetime import date

from django.shortcuts import render

from db.database import get_connection


def band_list(request):
    """Список групп из таблицы bands."""
    conn = get_connection()
    try:
        bands_list = conn.execute(
            """
SELECT
id,
name,
foundation_date,
required_instrument,
is_active
FROM bands
ORDER BY name;
"""
        ).fetchall()
    finally:
        conn.close()
    context = {
        "bands": bands_list,
    }
    return render(request, "bands/band_list.html", context)


def band_detail(request, band_id):
    """Страница группы из SQLite, 404 если не найдена."""
    conn = get_connection()
    try:
        band = conn.execute(
            """
SELECT
id,
name,
foundation_date,
required_instrument,
is_active
FROM bands
WHERE id = ?;
""",
            [band_id],
        ).fetchone()
        if band is None:
            members_count = 0
            available = False
        else:
            members_count = conn.execute(
                """
SELECT COUNT(*)
FROM members
WHERE band_id = ?;
""",
                [band_id],
            ).fetchone()[0]
            busy = conn.execute(
                """
SELECT COUNT(*)
FROM rehearsals
WHERE band_id = ?
AND rehearsal_date = ?
AND is_cancelled = 0;
""",
                [band_id, date.today().isoformat()],
            ).fetchone()[0]
            available = busy == 0
    finally:
        conn.close()
    if band is None:
        context = {"band": None}
    else:
        context = {
            "band": band,
            "members_count": members_count,
            "available": available,
        }
    return render(
        request,
        "bands/band_detail.html",
        context,
        status=404 if band is None else 200,
    )


def available_bands(request):
    """Поиск свободных групп на выбранную дату."""
    booking_date = request.GET.get("date")
    bands_list = []
    if booking_date:
        conn = get_connection()
        try:
            bands_list = conn.execute(
                """
SELECT
bands.id,
bands.name,
bands.required_instrument
FROM bands
WHERE bands.id NOT IN (
SELECT rehearsals.band_id
FROM rehearsals
WHERE rehearsals.rehearsal_date = ?
AND rehearsals.is_cancelled = 0
)
ORDER BY bands.name;
""",
                [booking_date],
            ).fetchall()
        finally:
            conn.close()
    return render(
        request,
        "bands/available.html",
        {
            "bands": bands_list,
            "booking_date": booking_date,
        },
    )
