"""Применить схему из sql/schema.sql к data/bands.sqlite (ПР7)."""

import sqlite3

conn = sqlite3.connect("data/bands.sqlite")
with open("sql/schema.sql", encoding="utf-8") as f:
    sql = f.read()
conn.executescript(sql)
conn.commit()
conn.close()
print("schema applied")
