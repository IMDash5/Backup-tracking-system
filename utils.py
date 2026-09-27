from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число, повторяя запрос при ошибке."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число")


def input_float(prompt: str) -> float:
    """Запросить у пользователя дробное число, повторяя запрос при ошибке."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите число (например, 12.5)")


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате ДД.ММ.ГГГГ."""
    while True:
        raw = input(prompt)
        try:
            return datetime.strptime(raw, "%d.%m.%Y").date()
        except ValueError:
            print(
                "Ошибка: введите дату в формате ДД.ММ.ГГГГ, "
                "например 21.09.2026"
            )
