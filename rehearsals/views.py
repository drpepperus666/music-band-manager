"""Страницы репетиций: данные из SQLite (ПР7)."""

from django.shortcuts import render

from db.database import get_connection


def rehearsal_list(request):
    """Список активных репетиций (JOIN bands)."""
    conn = get_connection()
    try:
        rehearsals_list = conn.execute(
            """
SELECT
rehearsals.id,
rehearsals.rehearsal_date,
rehearsals.participants,
rehearsals.is_cancelled,
bands.name AS band_name
FROM rehearsals
JOIN bands
ON rehearsals.band_id = bands.id
WHERE rehearsals.is_cancelled = 0
ORDER BY rehearsals.rehearsal_date;
"""
        ).fetchall()
    finally:
        conn.close()
    context = {
        "rehearsals": rehearsals_list,
    }
    return render(request, "rehearsals/rehearsal_list.html", context)


def rehearsal_detail(request, rehearsal_id):
    """Страница репетиции из SQLite, 404 если не найдена."""
    conn = get_connection()
    try:
        rehearsal = conn.execute(
            """
SELECT
rehearsals.id,
rehearsals.rehearsal_date,
rehearsals.participants,
rehearsals.is_cancelled,
bands.name AS band_name
FROM rehearsals
JOIN bands
ON rehearsals.band_id = bands.id
WHERE rehearsals.id = ?;
""",
            [rehearsal_id],
        ).fetchone()
    finally:
        conn.close()
    context = {
        "rehearsal": rehearsal,
    }
    return render(
        request,
        "rehearsals/rehearsal_detail.html",
        context,
        status=404 if rehearsal is None else 200,
    )


def statistics(request):
    """Статистика: количество репетиций по группам."""
    conn = get_connection()
    try:
        statistics_data = conn.execute(
            """
SELECT
bands.name AS band_name,
COUNT(rehearsals.id) AS rehearsals_count
FROM bands
LEFT JOIN rehearsals
ON bands.id = rehearsals.band_id
AND rehearsals.is_cancelled = 0
GROUP BY bands.id, bands.name
ORDER BY rehearsals_count DESC;
"""
        ).fetchall()
    finally:
        conn.close()
    return render(
        request,
        "rehearsals/statistics.html",
        {"statistics": statistics_data},
    )
