from datetime import date

from servers import (
    add_server,
    check_server_capacity,
    filter_servers_by_capacity,
    find_server,
    sort_servers,
)
from backups import (
    cancel_backup,
    check_backup_size,
    create_backup,
    get_backup_age,
    get_backup_status,
    get_backups_by_server,
    get_total_backup_size,
)
from storage import load_backups, load_servers, save_backups, save_servers
from utils import input_date, input_float, input_int

SERVERS_FILE = "data/servers.json"
BACKUPS_FILE = "data/backups.json"

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
0. Выход
"""


def show_servers(servers: dict[int, dict]) -> None:
    """Вывести список серверов в виде таблицы."""
    if not servers:
        print("Серверы не добавлены")
        return
    print(f"{'ID':<4}{'Название':<28}{'Хранилище, ГБ':<15}")
    for server_id, data in servers.items():
        print(
            f"{server_id:<4}{data['name']:<28}{data['storage_capacity']:<15}"
        )


def show_backups(backups: list[dict], servers: dict[int, dict]) -> None:
    """Вывести список резервных копий с указанием сервера и даты."""
    if not backups:
        print("Резервные копии отсутствуют")
        return
    for backup in backups:
        server_name = servers.get(backup["server_id"], {}).get(
            "name", "неизвестный сервер"
        )
        print(
            f"#{backup['id']} | {server_name} | "
            f"{backup['backup_date']} | {backup['size']} ГБ"
        )


def handle_check_capacity(servers: dict[int, dict]) -> None:
    """Обработать пункт меню «Проверить место на сервере»."""
    server_id = input_int("ID сервера: ")
    size = input_float("Требуемый размер, ГБ: ")
    try:
        if check_server_capacity(servers, server_id, size):
            print("Достаточно места для хранения резервной копии")
        else:
            print("Недостаточно места для хранения резервной копии")
    except KeyError as error:
        print(f"Ошибка: {error}")


def handle_create_backup(
    servers: dict[int, dict], backups: list[dict]
) -> None:
    """Обработать пункт меню «Создать резервную копию»."""
    server_id = input_int("ID сервера: ")
    if server_id not in servers:
        print("Сервер с таким ID не найден")
        return

    backup_date = input_date("Дата резервной копии (ДД.ММ.ГГГГ): ")
    size = input_float("Размер резервной копии, ГБ: ")

    print(check_backup_size(size, servers[server_id]["storage_capacity"]))
    if size > servers[server_id]["storage_capacity"]:
        return

    try:
        create_backup(backups, server_id, backup_date, size)
        print(get_backup_status(True))
        save_backups(BACKUPS_FILE, backups)
    except ValueError as error:
        print(get_backup_status(False))
        print(f"Причина: {error}")


def handle_server_statistics(
    servers: dict[int, dict], backups: list[dict]
) -> None:
    """Обработать пункт меню «Статистика по серверу»."""
    server_id = input_int("ID сервера: ")
    if server_id not in servers:
        print("Сервер с таким ID не найден")
        return
    server_backups = get_backups_by_server(backups, server_id)
    total_size = get_total_backup_size(backups, server_id)
    print(f"Количество резервных копий: {len(server_backups)}")
    print(f"Суммарный размер: {total_size} ГБ")
    if server_backups:
        last_backup = max(server_backups, key=lambda b: b["backup_date"])
        last_date = date.fromisoformat(last_backup["backup_date"])
        print(get_backup_age(last_date, date.today()))


def main() -> None:
    """Точка запуска приложения: меню и вызов функций проекта."""
    servers = load_servers(SERVERS_FILE)
    backups = load_backups(BACKUPS_FILE)

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
            handle_create_backup(servers, backups)

        elif choice == "5":
            backup_id = input_int("ID резервной копии для отмены: ")
            try:
                cancel_backup(backups, backup_id)
                print("Резервная копия отменена")
                save_backups(BACKUPS_FILE, backups)
            except KeyError as error:
                print(f"Ошибка: {error}")

        elif choice == "6":
            show_backups(backups, servers)

        elif choice == "7":
            handle_server_statistics(servers, backups)

        elif choice == "8":
            name = input("Название сервера: ")
            capacity = input_float("Объём хранилища, ГБ: ")
            server_id = add_server(servers, name, capacity)
            print(f"Сервер добавлен, ID = {server_id}")
            save_servers(SERVERS_FILE, servers)

        elif choice == "9":
            for server_id, data in sort_servers(servers):
                print(
                    f"{server_id}: {data['name']} — "
                    f"{data['storage_capacity']} ГБ"
                )

        elif choice == "10":
            min_capacity = input_float("Минимальный объём, ГБ: ")
            show_servers(filter_servers_by_capacity(servers, min_capacity))

        elif choice == "0":
            save_servers(SERVERS_FILE, servers)
            save_backups(BACKUPS_FILE, backups)
            print("Данные сохранены. До свидания!")
            break

        else:
            print("Неверный выбор, попробуйте снова")


if __name__ == "__main__":
    main()
