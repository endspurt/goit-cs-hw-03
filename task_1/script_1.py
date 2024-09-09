import psycopg2
import os
from dotenv import load_dotenv

# Завантаження змінних з файлу .env
load_dotenv()

# Підключення до бази даних PostgreSQL
connection = psycopg2.connect(
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cursor = connection.cursor()

# Створення таблиці користувачів (users)
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100),
    email VARCHAR(100) UNIQUE
);
"""

# Створення таблиці статусів (status)
create_status_table = """
CREATE TABLE IF NOT EXISTS status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE
);
"""

# Створення таблиці завдань (tasks)
create_tasks_table = """
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    status_id INTEGER REFERENCES status(id),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
"""

# Виконання SQL-запитів для створення таблиць
cursor.execute(create_users_table)
cursor.execute(create_status_table)
cursor.execute(create_tasks_table)

# Збереження змін
connection.commit()

# Закриття з'єднання
cursor.close()
connection.close()

print("Таблиці успішно створені.")
