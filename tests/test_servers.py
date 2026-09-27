from servers import (
    add_server,
    check_server_capacity,
    filter_servers_by_capacity,
    find_server,
    sort_servers,
)


def test_add_server():
    servers = {}
    add_server(servers, "Сервер бухгалтерии", 50)
    assert len(servers) == 1


def test_find_server():
    servers = {}
    add_server(servers, "Сервер бухгалтерии", 50)
    assert find_server(servers, "бухгалтерии")


def test_check_server_capacity():
    servers = {}
    server_id = add_server(servers, "Сервер отдела кадров", 100)
    assert check_server_capacity(servers, server_id, 80)


def test_filter_servers_by_capacity():
    servers = {}
    add_server(servers, "Сервер A", 20)
    add_server(servers, "Сервер B", 80)
    filtered = filter_servers_by_capacity(servers, 50)
    assert len(filtered) == 1


def test_sort_servers():
    servers = {}
    add_server(servers, "Сервер A", 20)
    add_server(servers, "Сервер B", 80)
    sorted_result = sort_servers(servers)
    assert sorted_result[0][1]["storage_capacity"] == 80
