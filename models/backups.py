from datetime import date
from typing import List, Optional

from .operators import Operator
from .servers import Server


class Backup:
    """Резервная копия сервера."""

    def __init__(
        self,
        backup_id: int,
        server: Server,
        backup_date: date,
        size: float,
        operator: Operator,
    ) -> None:
        """Создать объект резервной копии.

        Сохраняет идентификатор, сервер, дату, размер и оператора,
        создавшего копию.
        """
        self.id = backup_id
        self.server = server
        self.backup_date = backup_date
        self.size = size
        self.operator = operator
        self.is_cancelled = False

    def cancel(self) -> None:
        """Отменить резервную копию.

        Копия не удаляется из коллекции, а помечается как отменённая.
        """
        self.is_cancelled = True

    def __str__(self) -> str:
        """Вернуть строковое представление резервной копии."""
        status = "отменена" if self.is_cancelled else "активна"
        return (
            f"#{self.id} | {self.server.name} | {self.backup_date} | "
            f"{self.size} ГБ | оператор: {self.operator.name} | {status}"
        )


def is_backup_available(
    backups: List[Backup], server: Server, backup_date: date
) -> bool:
    """Проверить, можно ли создать резервную копию сервера на указанную дату.

    Возвращает False, если для этого сервера на эту дату уже есть
    активная (неотменённая) резервная копия.
    """
    for backup in backups:
        same_server = backup.server.id == server.id
        same_date = backup.backup_date == backup_date
        if same_server and same_date and not backup.is_cancelled:
            return False
    return True


def create_backup(
    backups: List[Backup],
    server: Server,
    backup_date: date,
    size: float,
    operator: Operator,
) -> Optional[Backup]:
    """Создать резервную копию и добавить её в коллекцию.

    Возвращает созданный объект Backup, либо None, если на указанную
    дату для сервера уже существует активная резервная копия.
    """
    if not is_backup_available(backups, server, backup_date):
        return None
    backup_id = max((backup.id for backup in backups), default=0) + 1
    backup = Backup(backup_id, server, backup_date, size, operator)
    backups.append(backup)
    return backup


def find_backup_by_id(
    backups: List[Backup], backup_id: int
) -> Optional[Backup]:
    """Найти резервную копию по идентификатору."""
    for backup in backups:
        if backup.id == backup_id:
            return backup
    return None


def cancel_backup(backups: List[Backup], backup_id: int) -> bool:
    """Найти резервную копию по идентификатору и отменить её.

    Возвращает True, если копия найдена и отменена, иначе False.
    """
    backup = find_backup_by_id(backups, backup_id)
    if backup is None:
        return False
    backup.cancel()
    return True


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


def get_backups_by_server(
    backups: List[Backup], server: Server
) -> List[Backup]:
    """Вернуть список резервных копий указанного сервера."""
    return [backup for backup in backups if backup.server.id == server.id]


def get_total_backup_size(backups: List[Backup], server: Server) -> float:
    """Посчитать суммарный размер активных резервных копий сервера."""
    server_backups = get_backups_by_server(backups, server)
    return sum(
        backup.size for backup in server_backups if not backup.is_cancelled
    )
