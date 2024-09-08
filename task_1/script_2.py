from faker import Faker
import psycopg2

fake = Faker()

# Підключення до бази даних PostgreSQL
connection = psycopg2.connect(
    database="deine_datenbank", 
    user="dein_benutzer", 
    password="dein_passwort", 
    host="localhost", 
    port="5432"
)

cursor = connection.cursor()

# Додавання початкових даних у таблицю статусів
statuses = ['new', 'in progress', 'completed']
for status in statuses:
    cursor.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT DO NOTHING;", (status,))

# Генерація випадкових користувачів та завдань
for _ in range(10):  # 10 випадкових користувачів
    fullname = fake.name()
    email = fake.email()

    # Додавання користувача до таблиці users
    cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id;", (fullname, email))
    user_id = cursor.fetchone()[0]

    # Кожному користувачу присвоюється 3 завдання
    for _ in range(3):
        title = fake.sentence(nb_words=4)
        description = fake.paragraph(nb_sentences=3)
        status_id = fake.random_int(min=1, max=3)  # Випадковий статус

        # Додавання завдання до таблиці tasks
        cursor.execute("""
            INSERT INTO tasks (title, description, status_id, user_id)
            VALUES (%s, %s, %s, %s);
        """, (title, description, status_id, user_id))

# Збереження змін у базі даних
connection.commit()

# Закриття з'єднання
cursor.close()
connection.close()

print("Початкові дані успішно додані.")
