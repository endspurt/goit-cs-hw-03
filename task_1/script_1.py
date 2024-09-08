import psycopg2

# Підключення до бази даних PostgreSQL
connection = psycopg2.connect(
    database="deine_datenbank", 
    user="dein_benutzer", 
    password="dein_passwort", 
    host="localhost", 
    port="5432"
)

cursor = connection.cursor()

# SQL-команди для створення таблиць
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100),
    email VARCHAR(100) UNIQUE
);
"""

create_status_table = """
CREATE TABLE IF NOT EXISTS status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE
);
"""

create_tasks_table = """
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    status_id INTEGER REFERENCES status(id),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
"""

# Створення таблиць у базі даних
cursor.execute(create_users_table)
cursor.execute(create_status_table)
cursor.execute(create_tasks_table)

# Збереження змін у базі даних
connection.commit()

# Закриття з'єднання
cursor.close()
connection.close()

print("Таблиці успішно створені.")
