from datetime import date


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число с обработкой ошибок."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print('Ошибка: введите целое число.')


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате YYYY-MM-DD
    с обработкой ошибок."""
    while True:
        try:
            return date.fromisoformat(input(prompt))
        except ValueError:
            print('Ошибка: введите дату в формате YYYY-MM-DD.')


def input_string(prompt: str) -> str:
    """Запросить строку у пользователя."""
    return input(prompt).strip()


def input_float(prompt: str) -> float:
    """Запросить у пользователя дробное число с обработкой ошибок."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print('Ошибка: введите число.')
