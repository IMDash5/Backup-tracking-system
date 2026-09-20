from datetime import date

server_name = "Сервер бухгалтерии"
backup_date = date(2026, 9, 18)
backup_size = 25.5
storage_available = 50
is_backup_available = True


def get_backup_status(is_backup_available):
    if is_backup_available:
        return "Резервная копия доступна"
    return "Резервная копия отсутствует"


def check_backup_size(backup_size, storage_available):
    if backup_size <= storage_available:
        return "Достаточно места для хранения резервной копии"
    return "Недостаточно места для хранения резервной копии"


def get_backup_age(backup_date, current_date):
    days_passed = (current_date - backup_date).days

    if days_passed <= 3:
        return "Резервная копия актуальна"
    return "Резервная копия устарела"


current_date = date(2026, 9, 21)

print(f"Сервер: {server_name}")
print(f"Дата резервной копии: {backup_date}")
print(f"Размер резервной копии: {backup_size} ГБ")
print()

print(get_backup_status(is_backup_available))
print(check_backup_size(backup_size, storage_available))
print(get_backup_age(backup_date, current_date))