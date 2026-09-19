import json


def load_bands(filename: str) -> list[dict]:
    """Загрузить группы из JSON-файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_bands(filename: str, bands: list[dict]) -> None:
    """Сохранить группы в JSON-файл."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(bands, f, ensure_ascii=False, indent=2)


def load_members(filename: str) -> list[dict]:
    """Загрузить кандидатов из JSON-файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_members(filename: str, members: list[dict]) -> None:
    """Сохранить кандидатов в JSON-файл."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(members, f, ensure_ascii=False, indent=2)


def load_rehearsals(filename: str) -> list[dict]:
    """Загрузить репетиции из JSON-файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_rehearsals(filename: str, rehearsals: list[dict]) -> None:
    """Сохранить репетиции в JSON-файл."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(rehearsals, f, ensure_ascii=False, indent=2)
