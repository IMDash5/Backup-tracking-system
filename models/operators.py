from typing import List, Optional


class Operator:
    """Оператор — сотрудник, создающий и отменяющий резервные копии."""

    def __init__(self, operator_id: int, name: str, email: str) -> None:
        """Создать объект оператора.

        Сохраняет переданные данные в атрибутах объекта.
        """
        self.id = operator_id
        self.name = name
        self.email = email

    def __str__(self) -> str:
        """Вернуть строковое представление оператора."""
        return f"{self.name} <{self.email}>"

    @classmethod
    def from_data(cls, data: dict) -> "Operator":
        """Создать оператора из словаря данных (например, из JSON)."""
        return cls(
            operator_id=data["id"],
            name=data["name"],
            email=data["email"],
        )


def add_operator(operators: List[Operator], name: str, email: str) -> Operator:
    """Создать объект Operator и добавить его в коллекцию.

    Идентификатор формируется автоматически. Возвращает созданный объект.
    """
    operator_id = max((operator.id for operator in operators), default=0) + 1
    operator = Operator(operator_id, name, email)
    operators.append(operator)
    return operator


def find_operator(operators: List[Operator], query: str) -> List[Operator]:
    """Найти операторов по подстроке имени или email (без учёта регистра)."""
    query_lower = query.lower()
    return [
        operator
        for operator in operators
        if query_lower in operator.name.lower()
        or query_lower in operator.email.lower()
    ]


def find_operator_by_id(
    operators: List[Operator], operator_id: int
) -> Optional[Operator]:
    """Найти оператора по идентификатору."""
    for operator in operators:
        if operator.id == operator_id:
            return operator
    return None
