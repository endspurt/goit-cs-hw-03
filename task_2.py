from pymongo import MongoClient
from bson.objectid import ObjectId

# Підключення до MongoDB
def connect_to_mongo():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["cat_database"]
        return db["cats"]
    except Exception as e:
        print(f"Помилка підключення до MongoDB: {e}")
        return None

# Створення нового запису в колекції (Create)
def create_cat(collection, name, age, features):
    try:
        cat = {
            "name": name,
            "age": age,
            "features": features
        }
        result = collection.insert_one(cat)
        print(f"Кіт доданий з ID: {result.inserted_id}")
    except Exception as e:
        print(f"Помилка створення кота: {e}")

# Читання всіх записів (Read)
def read_all_cats(collection):
    try:
        cats = collection.find()
        for cat in cats:
            print(cat)
    except Exception as e:
        print(f"Помилка читання всіх котів: {e}")

# Читання конкретного кота за ім'ям (Read)
def read_cat_by_name(collection, name):
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except Exception as e:
        print(f"Помилка читання кота з ім'ям {name}: {e}")

# Оновлення віку кота за ім'ям (Update)
def update_cat_age(collection, name, new_age):
    try:
        result = collection.update_one(
            {"name": name}, 
            {"$set": {"age": new_age}}
        )
        if result.matched_count > 0:
            print(f"Вік кота {name} оновлено до {new_age}.")
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except Exception as e:
        print(f"Помилка оновлення віку кота: {e}")

# Додавання нової характеристики до списку (Update)
def add_feature_to_cat(collection, name, new_feature):
    try:
        result = collection.update_one(
            {"name": name}, 
            {"$addToSet": {"features": new_feature}}  # Додає нову характеристику до списку
        )
        if result.matched_count > 0:
            print(f"Характеристика {new_feature} додана до кота {name}.")
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except Exception as e:
        print(f"Помилка додавання характеристики: {e}")

# Видалення кота за ім'ям (Delete)
def delete_cat_by_name(collection, name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Кота з ім'ям {name} видалено.")
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except Exception as e:
        print(f"Помилка видалення кота з ім'ям {name}: {e}")

# Видалення всіх записів у колекції (Delete)
def delete_all_cats(collection):
    try:
        result = collection.delete_many({})
        print(f"Видалено {result.deleted_count} котів.")
    except Exception as e:
        print(f"Помилка видалення всіх котів: {e}")

# Основна функція для запуску операцій CRUD
if __name__ == "__main__":
    collection = connect_to_mongo()
    if collection:
        # Створення нового кота
        create_cat(collection, "barsik", 3, ["ходит в капці", "дає себе гладити", "рудий"])

        # Виведення всіх котів
        print("Всі коти в базі даних:")
        read_all_cats(collection)

        # Виведення конкретного кота
        print("Інформація про кота barsik:")
        read_cat_by_name(collection, "barsik")

        # Оновлення віку кота
        update_cat_age(collection, "barsik", 4)

        # Додавання нової характеристики
        add_feature_to_cat(collection, "barsik", "любит гратись")

        # Видалення кота за ім'ям
        delete_cat_by_name(collection, "barsik")

        # Видалення всіх котів
        delete_all_cats(collection)
