import json
from datetime import date
from pathlib import Path
from typing import List

from models.backups import Backup
from models.operators import find_operator_by_id, Operator
from models.servers import find_server_by_id, Server


def load_servers(filename: str) -> List[Server]:
    """Загрузить серверы из JSON-файла и создать объекты Server.

    При отсутствии файла или некорректном JSON возвращает пустой список.
    """
    path = Path(filename)
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print(
            f"Предупреждение: файл {filename} повреждён, "
            "будет создан заново"
        )
        return []
    return [Server.from_data(item) for item in data]


def save_servers(filename: str, servers: List[Server]) -> None:
    """Сохранить объекты Server в JSON-файл."""
    data = [
        {
            "id": server.id,
            "name": server.name,
            "storage_capacity": server.storage_capacity,
        }
        for server in servers
    ]
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_backups(
    filename: str, servers: List[Server], operators: List[Operator]
) -> List[Backup]:
    """Загрузить резервные копии из JSON-файла и создать объекты Backup.

    Для каждой записи по server_id и operator_id ищутся соответствующие
    объекты Server и Operator. Если сервер или оператор не найдены,
    запись пропускается. При отсутствии файла или некорректном JSON
    возвращается пустой список.
    """
    path = Path(filename)
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print(
            f"Предупреждение: файл {filename} повреждён, "
            "будет создан заново"
        )
        return []

    backups: List[Backup] = []
    for item in data:
        server = find_server_by_id(servers, item["server_id"])
        if server is None:
            print(
                f"Предупреждение: сервер id={item['server_id']} не найден, "
                f"резервная копия id={item['id']} пропущена"
            )
            continue
        operator = find_operator_by_id(operators, item["operator_id"])
        if operator is None:
            print(
                f"Предупреждение: оператор id={item['operator_id']} не "
                f"найден, резервная копия id={item['id']} пропущена"
            )
            continue
        backup = Backup(
            backup_id=item["id"],
            server=server,
            backup_date=date.fromisoformat(item["backup_date"]),
            size=item["size"],
            operator=operator,
        )
        backup.is_cancelled = item.get("is_cancelled", False)
        backups.append(backup)
    return backups


def save_backups(filename: str, backups: List[Backup]) -> None:
    """Сохранить объекты Backup в JSON-файл.

    Ссылки на объекты Server и Operator преобразуются в их
    идентификаторы server_id и operator_id.
    """
    data = [
        {
            "id": backup.id,
            "server_id": backup.server.id,
            "backup_date": backup.backup_date.isoformat(),
            "size": backup.size,
            "operator_id": backup.operator.id,
            "is_cancelled": backup.is_cancelled,
        }
        for backup in backups
    ]
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_operators(filename: str) -> List[Operator]:
    """Загрузить операторов из JSON-файла и создать объекты Operator.

    При отсутствии файла или некорректном JSON возвращает пустой список.
    """
    path = Path(filename)
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print(
            f"Предупреждение: файл {filename} повреждён, "
            "будет создан заново"
        )
        return []
    return [Operator.from_data(item) for item in data]


def save_operators(filename: str, operators: List[Operator]) -> None:
    """Сохранить объекты Operator в JSON-файл."""
    data = [
        {
            "id": operator.id,
            "name": operator.name,
            "email": operator.email,
        }
        for operator in operators
    ]
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
