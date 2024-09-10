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

# 1. Отримати всі завдання певного користувача
user_id = 1
cursor.execute("SELECT * FROM tasks WHERE user_id = %s;", (user_id,))
tasks = cursor.fetchall()
print(f"Завдання користувача з ID {user_id}:")
for task in tasks:
    print(task)

# 2. Вибрати завдання за певним статусом (наприклад, 'new')
cursor.execute("SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'new');")
new_tasks = cursor.fetchall()
print("Завдання зі статусом 'new':")
for task in new_tasks:
    print(task)

# 3. Оновити статус конкретного завдання (на 'in progress')
task_id = 1
cursor.execute("UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = 'in progress') WHERE id = %s;", (task_id,))
print(f"Статус завдання з ID {task_id} оновлено до 'in progress'.")

# 4. Отримати список користувачів, які не мають жодного завдання
cursor.execute("SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);")
users_without_tasks = cursor.fetchall()
print("Користувачі без завдань:")
for user in users_without_tasks:
    print(user)

# 5. Додати нове завдання для конкретного користувача
cursor.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);",
               ('Нове завдання', 'Опис завдання', 1, user_id))
print("Нове завдання додано.")

# 6. Отримати всі завдання, які ще не завершено
cursor.execute("SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed');")
incomplete_tasks = cursor.fetchall()
print("Незавершені завдання:")
for task in incomplete_tasks:
    print(task)

# 7. Видалити конкретне завдання
task_id_to_delete = 1
cursor.execute("DELETE FROM tasks WHERE id = %s;", (task_id_to_delete,))
print(f"Завдання з ID {task_id_to_delete} видалено.")

# 8. Знайти користувачів з певною електронною поштою
cursor.execute("SELECT * FROM users WHERE email LIKE %s;", ('%@example.com',))
users_with_email = cursor.fetchall()
print("Користувачі з доменом '@example.com':")
for user in users_with_email:
    print(user)

# 9. Оновити ім'я користувача
cursor.execute("UPDATE users SET fullname = %s WHERE id = %s;", ('Новий Користувач', user_id))
print(f"Ім'я користувача з ID {user_id} оновлено.")

# 10. Отримати кількість завдань для кожного статусу
cursor.execute("SELECT status.name, COUNT(tasks.id) FROM tasks JOIN status ON tasks.status_id = status.id GROUP BY status.name;")
tasks_per_status = cursor.fetchall()
print("Кількість завдань для кожного статусу:")
for status in tasks_per_status:
    print(status)

# 11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
cursor.execute("""
    SELECT tasks.* FROM tasks
    JOIN users ON tasks.user_id = users.id
    WHERE users.email LIKE %s;
""", ('%@example.com',))
tasks_for_email_domain = cursor.fetchall()
print("Завдання користувачів з доменом '@example.com':")
for task in tasks_for_email_domain:
    print(task)

# 12. Отримати список завдань, що не мають опису
cursor.execute("SELECT * FROM tasks WHERE description IS NULL OR description = '';")
tasks_without_description = cursor.fetchall()
print("Завдання без опису:")
for task in tasks_without_description:
    print(task)

# 13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
cursor.execute("""
    SELECT users.fullname, tasks.title FROM tasks
    JOIN users ON tasks.user_id = users.id
    JOIN status ON tasks.status_id = status.id
    WHERE status.name = 'in progress';
""")
users_and_tasks_in_progress = cursor.fetchall()
print("Користувачі та їхні завдання у статусі 'in progress':")
for task in users_and_tasks_in_progress:
    print(task)

# 14. Отримати користувачів та кількість їхніх завдань
cursor.execute("""
    SELECT users.fullname, COUNT(tasks.id) AS task_count
    FROM users
    LEFT JOIN tasks ON users.id = tasks.user_id
    GROUP BY users.fullname;
""")
users_task_count = cursor.fetchall()

print("Кількість завдань для кожного користувача:")
for user in users_task_count:
    print(f"Користувач: {user[0]}, Кількість завдань: {user[1]}")

# Збереження змін
connection.commit()

# Закриття з'єднання
cursor.close()
connection.close()
