from models.servers import (
    add_server,
    filter_servers_by_capacity,
    find_server,
    find_server_by_id,
    sort_servers,
    Server
)


def test_server_creation():
    server = Server(1, "Сервер бухгалтерии", 50)
    assert server.id == 1
    assert server.name == "Сервер бухгалтерии"
    assert server.storage_capacity == 50


def test_server_has_free_space():
    server = Server(1, "Сервер бухгалтерии", 50)
    assert server.has_free_space(30)
    assert not server.has_free_space(60)


def test_server_validate_capacity():
    assert Server.validate_capacity(50)
    assert not Server.validate_capacity(-10)


def test_server_from_data():
    data = {"id": 1, "name": "Сервер отдела кадров", "storage_capacity": 100}
    server = Server.from_data(data)
    assert server.id == 1
    assert server.storage_capacity == 100


def test_add_server():
    servers = []
    add_server(servers, "Сервер отдела кадров", 100)
    assert len(servers) == 1


def test_find_server():
    servers = []
    add_server(servers, "Сервер бухгалтерии", 50)
    assert find_server(servers, "бухгалтерии")


def test_find_server_by_id():
    servers = []
    server = add_server(servers, "Сервер бухгалтерии", 50)
    assert find_server_by_id(servers, server.id) is server
    assert find_server_by_id(servers, 999) is None


def test_filter_servers_by_capacity():
    servers = []
    add_server(servers, "Сервер A", 20)
    add_server(servers, "Сервер B", 80)
    filtered = filter_servers_by_capacity(servers, 50)
    assert len(filtered) == 1


def test_sort_servers():
    servers = []
    add_server(servers, "Сервер A", 20)
    add_server(servers, "Сервер B", 80)
    sorted_servers = sort_servers(servers)
    assert sorted_servers[0].storage_capacity == 80
