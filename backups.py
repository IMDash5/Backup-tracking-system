from datetime import date


def is_backup_available(
    backups: list[dict], server_id: int, backup_date: date
) -> bool:
    """Проверить, можно ли создать резервную копию на указанную дату.

    Возвращает False, если резервная копия для этого сервера
    на эту дату уже существует.
    """
    target = backup_date.isoformat()
    for backup in backups:
        same_server = backup["server_id"] == server_id
        same_date = backup["backup_date"] == target
        if same_server and same_date:
            return False
    return True


def create_backup(
    backups: list[dict], server_id: int, backup_date: date, backup_size: float
) -> dict:
    """Создать резервную копию.

    Проверяет отсутствие резервной копии на эту дату и добавляет
    новую запись в список backups. Возвращает созданную запись.
    """
    if not is_backup_available(backups, server_id, backup_date):
        raise ValueError(
            f"Резервная копия для сервера {server_id} "
            f"на {backup_date} уже существует"
        )
    backup_id = max((b["id"] for b in backups), default=0) + 1
    backup = {
        "id": backup_id,
        "server_id": server_id,
        "backup_date": backup_date.isoformat(),
        "size": backup_size,
    }
    backups.append(backup)
    return backup


def cancel_backup(backups: list[dict], backup_id: int) -> None:
    """Отменить (удалить) резервную копию по идентификатору."""
    for index, backup in enumerate(backups):
        if backup["id"] == backup_id:
            del backups[index]
            return
    raise KeyError(f"Резервная копия с id={backup_id} не найдена")


def get_backup_status(is_backup_available: bool) -> str:
    """Вернуть текстовый статус резервной копии (функция из ПР1)."""
    if is_backup_available:
        return "Резервная копия доступна"
    return "Резервная копия отсутствует"


def check_backup_size(backup_size: float, storage_available: float) -> str:
    """Проверить, хватает ли места для резервной копии (функция из ПР1)."""
    if backup_size <= storage_available:
        return "Достаточно места для хранения резервной копии"
    return "Недостаточно места для хранения резервной копии"


def get_backup_age(backup_date: date, current_date: date) -> str:
    """Определить актуальность резервной копии по её возрасту.

    Функция из ПР1.
    """
    days_passed = (current_date - backup_date).days
    if days_passed <= 3:
        return "Резервная копия актуальна"
    return "Резервная копия устарела"


def get_backups_by_server(backups: list[dict], server_id: int) -> list[dict]:
    """Вернуть список резервных копий указанного сервера."""
    return list(
        backup for backup in backups if backup["server_id"] == server_id
    )


def get_total_backup_size(backups: list[dict], server_id: int) -> float:
    """Посчитать суммарный размер резервных копий сервера."""
    server_backups = get_backups_by_server(backups, server_id)
    return sum(backup["size"] for backup in server_backups)
