from datetime import date
from typing import List

from models.backups import (
    Backup,
    cancel_backup,
    check_backup_size,
    create_backup,
    get_backup_age,
    get_backup_status,
    get_backups_by_server,
    get_total_backup_size,
)
from models.operators import add_operator, find_operator_by_id, Operator
from models.servers import (
    add_server,
    filter_servers_by_capacity,
    find_server,
    find_server_by_id,
    sort_servers,
    Server
)
from storage import (
    load_backups,
    load_operators,
    load_servers,
    save_backups,
    save_operators,
    save_servers,
)
from utils import input_date, input_float, input_int

SERVERS_FILE = "data/servers.json"
BACKUPS_FILE = "data/backups.json"
OPERATORS_FILE = "data/operators.json"

MENU = """
=== Система учёта резервных копий ===
1. Показать серверы
2. Найти сервер по названию
3. Проверить место на сервере
4. Создать резервную копию
5. Отменить резервную копию
6. Показать резервные копии
7. Статистика по серверу
8. Добавить сервер
9. Сортировать серверы по объёму хранилища
10. Отобрать серверы по минимальному объёму
11. Показать операторов
12. Добавить оператора
0. Выход
"""


def show_servers(servers: List[Server]) -> None:
    """Вывести список серверов, используя их строковое представление."""
    if not servers:
        print("Серверы не добавлены")
        return
    for server in servers:
        print(f"{server.id}: {server}")


def show_backups(backups: List[Backup]) -> None:
    """Вывести список резервных копий, используя их строковое представление."""
    if not backups:
        print("Резервные копии отсутствуют")
        return
    for backup in backups:
        print(backup)


def show_operators(operators: List[Operator]) -> None:
    """Вывести список операторов, используя их строковое представление."""
    if not operators:
        print("Операторы не добавлены")
        return
    for operator in operators:
        print(f"{operator.id}: {operator}")


def handle_check_capacity(servers: List[Server]) -> None:
    """Обработать пункт меню «Проверить место на сервере»."""
    server_id = input_int("ID сервера: ")
    server = find_server_by_id(servers, server_id)
    if server is None:
        print("Сервер с таким ID не найден")
        return
    size = input_float("Требуемый размер, ГБ: ")
    if server.has_free_space(size):
        print("Достаточно места для хранения резервной копии")
    else:
        print("Недостаточно места для хранения резервной копии")


def handle_create_backup(
    servers: List[Server], operators: List[Operator], backups: List[Backup]
) -> None:
    """Обработать пункт меню «Создать резервную копию»."""
    server_id = input_int("ID сервера: ")
    server = find_server_by_id(servers, server_id)
    if server is None:
        print("Сервер с таким ID не найден")
        return

    operator_id = input_int("ID оператора: ")
    operator = find_operator_by_id(operators, operator_id)
    if operator is None:
        print("Оператор с таким ID не найден")
        return

    backup_date = input_date("Дата резервной копии (ДД.ММ.ГГГГ): ")
    size = input_float("Размер резервной копии, ГБ: ")

    print(check_backup_size(size, server.storage_capacity))
    if not server.has_free_space(size):
        return

    backup = create_backup(backups, server, backup_date, size, operator)
    print(get_backup_status(backup is not None))
    if backup is None:
        print(
            "Причина: на эту дату для сервера уже есть "
            "активная резервная копия"
        )
    else:
        save_backups(BACKUPS_FILE, backups)


def handle_server_statistics(
    servers: List[Server], backups: List[Backup]
) -> None:
    """Обработать пункт меню «Статистика по серверу»."""
    server_id = input_int("ID сервера: ")
    server = find_server_by_id(servers, server_id)
    if server is None:
        print("Сервер с таким ID не найден")
        return
    server_backups = get_backups_by_server(backups, server)
    active_backups = [b for b in server_backups if not b.is_cancelled]
    total_size = get_total_backup_size(backups, server)
    print(f"Всего резервных копий: {len(server_backups)}")
    print(f"Из них активных: {len(active_backups)}")
    print(f"Суммарный размер активных копий: {total_size} ГБ")
    if active_backups:
        last_backup = max(active_backups, key=lambda b: b.backup_date)
        print(get_backup_age(last_backup.backup_date, date.today()))


def main() -> None:
    """Точка запуска приложения: меню и вызов функций проекта."""
    servers = load_servers(SERVERS_FILE)
    operators = load_operators(OPERATORS_FILE)
    backups = load_backups(BACKUPS_FILE, servers, operators)

    while True:
        print(MENU)
        choice = input("Выберите действие: ")

        if choice == "1":
            show_servers(servers)

        elif choice == "2":
            query = input("Название (или часть названия): ")
            show_servers(find_server(servers, query))

        elif choice == "3":
            handle_check_capacity(servers)

        elif choice == "4":
            handle_create_backup(servers, operators, backups)

        elif choice == "5":
            backup_id = input_int("ID резервной копии для отмены: ")
            if cancel_backup(backups, backup_id):
                print("Резервная копия отменена")
                save_backups(BACKUPS_FILE, backups)
            else:
                print("Резервная копия с таким ID не найдена")

        elif choice == "6":
            show_backups(backups)

        elif choice == "7":
            handle_server_statistics(servers, backups)

        elif choice == "8":
            name = input("Название сервера: ")
            capacity = input_float("Объём хранилища, ГБ: ")
            if not Server.validate_capacity(capacity):
                print("Ошибка: объём хранилища должен быть положительным")
                continue
            server = add_server(servers, name, capacity)
            print(f"Сервер добавлен, ID = {server.id}")
            save_servers(SERVERS_FILE, servers)

        elif choice == "9":
            for server in sort_servers(servers):
                print(server)

        elif choice == "10":
            min_capacity = input_float("Минимальный объём, ГБ: ")
            show_servers(filter_servers_by_capacity(servers, min_capacity))

        elif choice == "11":
            show_operators(operators)

        elif choice == "12":
            name = input("Имя оператора: ")
            email = input("Email оператора: ")
            operator = add_operator(operators, name, email)
            print(f"Оператор добавлен, ID = {operator.id}")
            save_operators(OPERATORS_FILE, operators)

        elif choice == "0":
            save_servers(SERVERS_FILE, servers)
            save_operators(OPERATORS_FILE, operators)
            save_backups(BACKUPS_FILE, backups)
            print("Данные сохранены. До свидания!")
            break

        else:
            print("Неверный выбор, попробуйте снова")


if __name__ == "__main__":
    main()
