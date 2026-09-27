def add_server(
    servers: dict[int, dict], server_name: str, storage_capacity: float
) -> int:
    """Добавить сервер в словарь servers.

    Формирует новый идентификатор сервера и добавляет его данные
    (название и объём хранилища) в словарь servers.
    Возвращает идентификатор добавленного сервера.
    """
    server_id = max(servers.keys(), default=0) + 1
    servers[server_id] = {
        "name": server_name,
        "storage_capacity": storage_capacity,
    }
    return server_id


def find_server(servers: dict[int, dict], query: str) -> dict[int, dict]:
    """Найти серверы по подстроке названия.

    Перебирает словарь servers и отбирает серверы, в названии которых
    встречается подстрока query (без учёта регистра).
    """
    query_lower = query.lower()
    return {
        server_id: data
        for server_id, data in servers.items()
        if query_lower in data["name"].lower()
    }


def check_server_capacity(
    servers: dict[int, dict], server_id: int, required_size: float
) -> bool:
    """Проверить, достаточно ли места на сервере.

    Возвращает True, если объём хранилища сервера не меньше required_size.
    """
    if server_id not in servers:
        raise KeyError(f"Сервер с id={server_id} не найден")
    return servers[server_id]["storage_capacity"] >= required_size


def filter_servers_by_capacity(
    servers: dict[int, dict], min_capacity: float
) -> dict[int, dict]:
    """Отобрать серверы, объём хранилища которых не меньше min_capacity."""
    return {
        server_id: data
        for server_id, data in servers.items()
        if data["storage_capacity"] >= min_capacity
    }


def sort_servers(servers: dict[int, dict]) -> list[tuple[int, dict]]:
    """Отсортировать серверы по объёму хранилища (по убыванию)."""
    return sorted(
        servers.items(),
        key=lambda item: item[1]["storage_capacity"],
        reverse=True,
    )
