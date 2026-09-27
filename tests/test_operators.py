from models.operators import (
    add_operator,
    find_operator,
    find_operator_by_id,
    Operator
)


def test_operator_creation():
    operator = Operator(1, "Иван Петров", "ivan@example.com")
    assert operator.id == 1
    assert operator.name == "Иван Петров"
    assert operator.email == "ivan@example.com"


def test_operator_from_data():
    data = {"id": 1, "name": "Анна Смирнова", "email": "anna@example.com"}
    operator = Operator.from_data(data)
    assert operator.id == 1
    assert operator.email == "anna@example.com"


def test_add_operator():
    operators = []
    add_operator(operators, "Иван Петров", "ivan@example.com")
    assert len(operators) == 1


def test_find_operator_by_name():
    operators = []
    add_operator(operators, "Иван Петров", "ivan@example.com")
    assert find_operator(operators, "иван")


def test_find_operator_by_email():
    operators = []
    add_operator(operators, "Иван Петров", "ivan@example.com")
    assert find_operator(operators, "ivan@")


def test_find_operator_by_id():
    operators = []
    operator = add_operator(operators, "Иван Петров", "ivan@example.com")
    assert find_operator_by_id(operators, operator.id) is operator
    assert find_operator_by_id(operators, 999) is None
