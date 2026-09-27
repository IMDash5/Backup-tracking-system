from datetime import date

from models.operators import Operator
from models.servers import Server
from models.backups import (
    cancel_backup,
    check_backup_size,
    create_backup,
    get_backup_age,
    get_backup_status,
    get_total_backup_size,
    is_backup_available,
)


def make_server() -> Server:
    return Server(1, "Сервер бухгалтерии", 50)


def make_operator() -> Operator:
    return Operator(1, "Иван Петров", "ivan@example.com")


def test_backup_creation():
    server = make_server()
    operator = make_operator()
    backup = create_backup([], server, date(2026, 9, 21), 10.0, operator)
    assert backup is not None
    assert backup.id == 1
    assert backup.server is server
    assert backup.operator is operator
    assert backup.backup_date == date(2026, 9, 21)
    assert not backup.is_cancelled


def test_backup_cancel():
    server = make_server()
    operator = make_operator()
    backups = []
    backup = create_backup(backups, server, date(2026, 9, 21), 10.0, operator)
    assert backup is not None
    backup.cancel()
    assert backup.is_cancelled


def test_is_backup_available():
    server = make_server()
    assert is_backup_available([], server, date(2026, 9, 21))


def test_duplicate_backup_forbidden():
    server = make_server()
    operator = make_operator()
    backups = []
    create_backup(backups, server, date(2026, 9, 21), 10.0, operator)
    assert not is_backup_available(backups, server, date(2026, 9, 21))
    second = create_backup(
        backups, server, date(2026, 9, 21), 5.0, operator
    )
    assert second is None


def test_cancelled_backup_frees_date():
    server = make_server()
    operator = make_operator()
    backups = []
    first = create_backup(
        backups, server, date(2026, 9, 21), 10.0, operator
    )
    assert first is not None
    first.cancel()
    assert is_backup_available(backups, server, date(2026, 9, 21))
    second = create_backup(
        backups, server, date(2026, 9, 21), 12.0, operator
    )
    assert second is not None


def test_cancel_backup_by_id():
    server = make_server()
    operator = make_operator()
    backups = []
    backup = create_backup(
        backups, server, date(2026, 9, 21), 10.0, operator
    )
    assert backup is not None
    assert cancel_backup(backups, backup.id)
    assert backup.is_cancelled
    assert not cancel_backup(backups, 999)


def test_get_total_backup_size_ignores_cancelled():
    server = make_server()
    operator = make_operator()
    backups = []
    first = create_backup(
        backups, server, date(2026, 9, 21), 10.0, operator
    )
    assert first is not None
    create_backup(backups, server, date(2026, 9, 22), 5.0, operator)
    first.cancel()
    assert get_total_backup_size(backups, server) == 5.0


def test_get_backup_status():
    assert get_backup_status(True) == "Резервная копия доступна"
    assert get_backup_status(False) == "Резервная копия отсутствует"


def test_check_backup_size():
    enough = "Достаточно места для хранения резервной копии"
    not_enough = "Недостаточно места для хранения резервной копии"
    assert check_backup_size(10, 50) == enough
    assert check_backup_size(60, 50) == not_enough


def test_get_backup_age():
    assert get_backup_age(date(2026, 9, 20), date(2026, 9, 21)) == (
        "Резервная копия актуальна"
    )
    assert get_backup_age(date(2026, 9, 1), date(2026, 9, 21)) == (
        "Резервная копия устарела"
    )
