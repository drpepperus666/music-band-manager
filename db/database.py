"""Подключение Python к SQLite (ПР7)."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "bands.sqlite"


def get_connection() -> sqlite3.Connection:
    """Создать соединение с проверкой внешних ключей."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn
