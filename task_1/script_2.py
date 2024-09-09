from faker import Faker
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
fake = Faker()

# Додавання статусів до таблиці status
statuses = ['new', 'in progress', 'completed']
for status in statuses:
    cursor.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT DO NOTHING;", (status,))

# Генерація випадкових користувачів і додавання їх до таблиці users
for _ in range(10):  # 10 випадкових користувачів
    fullname = fake.name()
    email = fake.email()

    cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id;", (fullname, email))
    user_id = cursor.fetchone()[0]

    # Додавання завдань для кожного користувача
    for _ in range(3):
        title = fake.sentence(nb_words=4)
        description = fake.paragraph(nb_sentences=3)
        status_id = fake.random_int(min=1, max=3)

        cursor.execute("""
            INSERT INTO tasks (title, description, status_id, user_id)
            VALUES (%s, %s, %s, %s);
        """, (title, description, status_id, user_id))

# Збереження змін
connection.commit()

# Закриття з'єднання
cursor.close()
connection.close()

print("Дані успішно додані.")
