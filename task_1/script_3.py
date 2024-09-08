import psycopg2

# Підключення до бази даних PostgreSQL
connection = psycopg2.connect(
    database="deine_datenbank", 
    user="dein_користувач", 
    password="твой_пароль", 
    host="localhost", 
    port="5432"
)

cursor = connection.cursor()

# Приклад запиту: отримати всі завдання конкретного користувача
user_id = 1  # Приклад: користувач з ID 1
cursor.execute("SELECT title, description FROM tasks WHERE user_id = %s;", (user_id,))
tasks = cursor.fetchall()

print(f"Завдання користувача з ID {user_id}:")
for task in tasks:
    print(f"- {task[0]}: {task[1]}")

# Приклад запиту: отримати завдання зі статусом 'in progress'
cursor.execute("SELECT title, description FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'in progress');")
in_progress_tasks = cursor.fetchall()

print("Завдання зі статусом 'in progress':")
for task in in_progress_tasks:
    print(f"- {task[0]}: {task[1]}")

# Тут можна додати інші SQL-запити...

# Закриття з'єднання
cursor.close()
connection.close()
