"""Загрузка и сохранение объектной модели в JSON (ПР3)."""

import json
from typing import Optional

from models.band import Band
from models.member import Member
from models.rehearsal import Rehearsal


def _load_json(filename: str):
    """Загрузить сырой JSON-список, вернуть [] при ошибках."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def _save_json(filename: str, data: list) -> None:
    """Сохранить список словарей в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_bands(filename: str) -> list:
    """Загрузить группы из JSON как объекты Band."""
    return [Band.from_data(item) for item in _load_json(filename)]


def save_bands(filename: str, bands: list) -> None:
    """Сохранить объекты Band в JSON."""
    _save_json(filename, [b.to_dict() for b in bands])


def load_members(filename: str, bands: Optional[list] = None) -> list:
    """Загрузить участников, связав с объектами Band."""
    bands = bands if bands is not None else []
    return [Member.from_data(item, bands) for item in _load_json(filename)]


def save_members(filename: str, members: list) -> None:
    """Сохранить объекты Member в JSON (band -> band_id)."""
    _save_json(filename, [m.to_dict() for m in members])


def load_rehearsals(filename: str, bands: Optional[list] = None) -> list:
    """Загрузить репетиции, связав с объектами Band."""
    bands = bands if bands is not None else []
    result = []
    for item in _load_json(filename):
        rehearsal = Rehearsal.from_data(item, bands)
        if rehearsal is not None:
            result.append(rehearsal)
    return result


def save_rehearsals(filename: str, rehearsals: list) -> None:
    """Сохранить объекты Rehearsal в JSON (band -> band_id)."""
    _save_json(filename, [r.to_dict() for r in rehearsals])
