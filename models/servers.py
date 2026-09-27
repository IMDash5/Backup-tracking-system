from typing import List, Optional


class Server:
    """Сервер, для которого ведётся учёт резервных копий."""

    def __init__(
        self, server_id: int, name: str, storage_capacity: float
    ) -> None:
        """Создать объект сервера.

        Сохраняет переданные данные в атрибутах объекта.
        """
        self.id = server_id
        self.name = name
        self.storage_capacity = storage_capacity

    def has_free_space(self, required_size: float) -> bool:
        """Проверить, достаточно ли места для копии заданного размера."""
        return self.storage_capacity >= required_size

    def __str__(self) -> str:
        """Вернуть строковое представление сервера."""
        return f"{self.name} (хранилище: {self.storage_capacity} ГБ)"

    @staticmethod
    def validate_capacity(capacity: float) -> bool:
        """Проверить корректность значения объёма хранилища."""
        return capacity > 0

    @classmethod
    def from_data(cls, data: dict) -> "Server":
        """Создать сервер из словаря данных (например, считанного из JSON)."""
        return cls(
            server_id=data["id"],
            name=data["name"],
            storage_capacity=data["storage_capacity"],
        )


def add_server(
    servers: List[Server], name: str, storage_capacity: float
) -> Server:
    """Создать объект Server и добавить его в коллекцию.

    Идентификатор формируется автоматически. Возвращает созданный объект.
    """
    server_id = max((server.id for server in servers), default=0) + 1
    server = Server(server_id, name, storage_capacity)
    servers.append(server)
    return server


def find_server(servers: List[Server], query: str) -> List[Server]:
    """Найти серверы по подстроке названия (без учёта регистра)."""
    query_lower = query.lower()
    return [server for server in servers if query_lower in server.name.lower()]


def find_server_by_id(
    servers: List[Server], server_id: int
) -> Optional[Server]:
    """Найти сервер по идентификатору."""
    for server in servers:
        if server.id == server_id:
            return server
    return None


def filter_servers_by_capacity(
    servers: List[Server], min_capacity: float
) -> List[Server]:
    """Отобрать серверы, объём хранилища которых не меньше min_capacity."""
    return [
        server for server in servers if server.storage_capacity >= min_capacity
    ]


def sort_servers(servers: List[Server]) -> List[Server]:
    """Отсортировать серверы по объёму хранилища (по убыванию)."""
    return sorted(
        servers, key=lambda server: server.storage_capacity, reverse=True
    )
