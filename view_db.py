# Для проверки содержимого БД
from app import app, db
from app.models import User


def print_db_structure_and_contents():
    # Выводим структуру базы данных
    print("Структура базы данных:")
    for table in db.metadata.sorted_tables:
        print(f"\nТаблица {table.name}:")
        for column in table.columns:
            print(f"  {column.name} ({column.type})")

    # Выводим содержимое таблиц
    print("\nСодержимое базы данных:")
    with app.app_context():
        users = User.query.all()
        if users:
            print("\nТаблица User:")
            for user in users:
                print(f"  id: {user.id}, username: {user.username}, email: {user.email}, password: {user.password}")
        else:
            print("\nТаблица User пуста.")


# Пример вызова функции
if __name__ == "__main__":
    print_db_structure_and_contents()
