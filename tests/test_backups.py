from datetime import date

from backups import (
    cancel_backup,
    check_backup_size,
    create_backup,
    get_backup_status,
    is_backup_available,
)


def test_is_backup_available():
    backups = []
    assert is_backup_available(backups, 1, date(2026, 9, 21))


def test_duplicate_backup_forbidden():
    backups = []
    create_backup(backups, 1, date(2026, 9, 21), 10.0)
    assert not is_backup_available(backups, 1, date(2026, 9, 21))


def test_cancel_backup():
    backups = []
    backup = create_backup(backups, 1, date(2026, 9, 21), 10.0)
    cancel_backup(backups, backup["id"])
    assert len(backups) == 0


def test_get_backup_status():
    assert get_backup_status(True) == "Резервная копия доступна"
    assert get_backup_status(False) == "Резервная копия отсутствует"


def test_check_backup_size():
    enough = "Достаточно места для хранения резервной копии"
    not_enough = "Недостаточно места для хранения резервной копии"
    assert check_backup_size(10, 50) == enough
    assert check_backup_size(60, 50) == not_enough
