import json
from pathlib import Path


def load_servers(filename: str) -> dict[int, dict]:
    """Загрузить серверы из JSON-файла.

    При отсутствии файла или некорректном JSON возвращает пустой словарь.
    """
    path = Path(filename)
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print(
            f"Предупреждение: файл {filename} повреждён, "
            "будет создан заново"
        )
        return {}
    return {
        int(server["id"]): {
            "name": server["name"],
            "storage_capacity": server["storage_capacity"],
        }
        for server in data
    }


def save_servers(filename: str, servers: dict[int, dict]) -> None:
    """Сохранить серверы в JSON-файл."""
    data = [
        {
            "id": server_id,
            "name": info["name"],
            "storage_capacity": info["storage_capacity"],
        }
        for server_id, info in servers.items()
    ]
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_backups(filename: str) -> list[dict]:
    """Загрузить резервные копии из JSON-файла.

    При отсутствии файла или некорректном JSON возвращает пустой список.
    """
    path = Path(filename)
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(
            f"Предупреждение: файл {filename} повреждён, "
            "будет создан заново"
        )
        return []


def save_backups(filename: str, backups: list[dict]) -> None:
    """Сохранить резервные копии в JSON-файл."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(backups, file, ensure_ascii=False, indent=2)
