-- ==========================================
-- Bandly: структура базы данных (ПР7)
-- ==========================================
CREATE TABLE IF NOT EXISTS bands (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
foundation_date TEXT NOT NULL,
required_instrument TEXT NOT NULL,
is_active INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS members (
id INTEGER PRIMARY KEY,
band_id INTEGER NOT NULL,
instrument TEXT NOT NULL,
experience_years INTEGER NOT NULL DEFAULT 0,
status TEXT NOT NULL DEFAULT '',
FOREIGN KEY (band_id) REFERENCES bands(id)
);
CREATE TABLE IF NOT EXISTS rehearsals (
id INTEGER PRIMARY KEY,
band_id INTEGER NOT NULL,
rehearsal_date TEXT NOT NULL,
participants INTEGER NOT NULL DEFAULT 0,
is_cancelled INTEGER NOT NULL DEFAULT 0,
FOREIGN KEY (band_id) REFERENCES bands(id)
);
