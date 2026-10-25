-- ==========================================
-- Bandly: SQL-запросы проекта (ПР7)
-- ==========================================

-- 1. Список групп (выборка, сортировка по названию)
SELECT
id,
name,
foundation_date,
required_instrument,
is_active
FROM bands
ORDER BY name;

-- 2. Список репетиций (выборка, сортировка по дате)
SELECT
id,
band_id,
rehearsal_date,
participants,
is_cancelled
FROM rehearsals
ORDER BY rehearsal_date;

-- 3. Активные группы (фильтрация WHERE по статусу)
SELECT
id,
name,
required_instrument
FROM bands
WHERE is_active = 1
ORDER BY name;

-- 4. Поиск групп по требуемому инструменту (фильтрация WHERE LIKE)
SELECT
id,
name,
required_instrument
FROM bands
WHERE required_instrument LIKE '%Гитара%'
ORDER BY name;

-- 5. Участники с названиями групп (соединение JOIN)
SELECT
members.id,
members.instrument,
members.experience_years,
bands.name AS band_name
FROM members
JOIN bands
ON members.band_id = bands.id
ORDER BY members.experience_years DESC;

-- 6. Активные репетиции с названиями групп (JOIN + WHERE)
SELECT
rehearsals.id,
rehearsals.rehearsal_date,
rehearsals.participants,
bands.name AS band_name
FROM rehearsals
JOIN bands
ON rehearsals.band_id = bands.id
WHERE rehearsals.is_cancelled = 0
ORDER BY rehearsals.rehearsal_date;

-- 7. Количество активных репетиций (агрегатная функция COUNT)
SELECT
COUNT(*) AS active_count
FROM rehearsals
WHERE is_cancelled = 0;

-- 8. Среднее число участников активных репетиций (агрегатная AVG)
SELECT
AVG(participants) AS avg_participants
FROM rehearsals
WHERE is_cancelled = 0;

-- 9. Количество репетиций по группам (группировка GROUP BY)
SELECT
bands.name AS band_name,
COUNT(rehearsals.id) AS rehearsals_count
FROM bands
LEFT JOIN rehearsals
ON bands.id = rehearsals.band_id
AND rehearsals.is_cancelled = 0
GROUP BY bands.id, bands.name
ORDER BY rehearsals_count DESC;

-- 10. Количество участников по инструментам (группировка GROUP BY)
SELECT
instrument,
COUNT(*) AS members_count
FROM members
GROUP BY instrument
ORDER BY members_count DESC;

-- 11. Группы с более чем одной активной репетицией (HAVING)
SELECT
bands.name AS band_name,
COUNT(rehearsals.id) AS rehearsals_count
FROM bands
JOIN rehearsals
ON bands.id = rehearsals.band_id
WHERE rehearsals.is_cancelled = 0
GROUP BY bands.id, bands.name
HAVING COUNT(rehearsals.id) > 1
ORDER BY rehearsals_count DESC;

-- 12. Свободные группы на выбранную дату (подзапрос NOT IN)
SELECT
bands.id,
bands.name,
bands.required_instrument
FROM bands
WHERE bands.id NOT IN (
SELECT rehearsals.band_id
FROM rehearsals
WHERE rehearsals.rehearsal_date = '2026-09-15'
AND rehearsals.is_cancelled = 0
)
ORDER BY bands.name;
