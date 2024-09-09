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

# SQL-запити для виконання:

# 1. Отримати всі завдання певного користувача
user_id = 1
cursor.execute("SELECT * FROM tasks WHERE user_id = %s;", (user_id,))
tasks = cursor.fetchall()
print(f"Завдання користувача з ID {user_id}:")
for task in tasks:
    print(task)

# 2. Отримати завдання зі статусом 'in progress'
cursor.execute("SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'in progress');")
tasks_in_progress = cursor.fetchall()
print("Завдання зі статусом 'in progress':")
for task in tasks_in_progress:
    print(task)

# 3. Оновити статус завдання на 'completed'
task_id = 1
cursor.execute("UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = 'completed') WHERE id = %s;", (task_id,))
print(f"Статус завдання з ID {task_id} оновлено до 'completed'.")

# 4. Отримати користувачів, які не мають завдань
cursor.execute("SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);")
users_without_tasks = cursor.fetchall()
print("Користувачі без завдань:")
for user in users_without_tasks:
    print(user)

# 5. Додати нове завдання для користувача
cursor.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);",
               ('Нове завдання', 'Опис завдання', 1, user_id))
print("Нове завдання додано.")

# Збереження змін
connection.commit()

# Закриття з'єднання
cursor.close()
connection.close()

