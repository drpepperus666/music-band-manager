"""Перенос данных из JSON в SQLite (ПР7)."""

import json

from db.database import get_connection

BANDS_FILE = "data/bands.json"
MEMBERS_FILE = "data/members.json"
REHEARSALS_FILE = "data/rehearsals.json"


def load_json(filename):
    """Прочитать JSON-список."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_bands(conn):
    """Перенести группы."""
    bands = load_json(BANDS_FILE)
    conn.execute("DELETE FROM rehearsals")
    conn.execute("DELETE FROM members")
    conn.execute("DELETE FROM bands")
    conn.executemany(
        """
INSERT INTO bands (
id,
name,
foundation_date,
required_instrument,
is_active
)
VALUES (?, ?, ?, ?, ?)
""",
        [
            (
                band["id"],
                band["name"],
                band.get("foundation_date", ""),
                band.get("required_instrument", ""),
                int(bool(band.get("is_active", False))),
            )
            for band in bands
        ],
    )


def import_members(conn):
    """Перенести участников."""
    members = load_json(MEMBERS_FILE)
    conn.executemany(
        """
INSERT INTO members (
id,
band_id,
instrument,
experience_years,
status
)
VALUES (?, ?, ?, ?, ?)
""",
        [
            (
                member["id"],
                member["band_id"],
                member.get("instrument", ""),
                int(member.get("experience_years", 0)),
                member.get("status", ""),
            )
            for member in members
        ],
    )


def import_rehearsals(conn):
    """Перенести репетиции."""
    rehearsals = load_json(REHEARSALS_FILE)
    conn.executemany(
        """
INSERT INTO rehearsals (
id,
band_id,
rehearsal_date,
participants,
is_cancelled
)
VALUES (?, ?, ?, ?, ?)
""",
        [
            (
                rehearsal["id"],
                rehearsal["band_id"],
                rehearsal.get("rehearsal_date", ""),
                int(rehearsal.get("participants", 0)),
                int(bool(rehearsal.get("is_cancelled", False))),
            )
            for rehearsal in rehearsals
        ],
    )


def main():
    """Выполнить импорт всех сущностей."""
    conn = get_connection()
    try:
        import_bands(conn)
        import_members(conn)
        import_rehearsals(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
