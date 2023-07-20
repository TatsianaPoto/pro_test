import argparse
import pymongo
import csv

def connect_to_mongodb():
    """Подключение к серверу MongoDB и базе данных."""
    client = pymongo.MongoClient("mongodb://localhost:22110/")
    db = client["car_database"]
    print("Подключение к базе данных успешно установлено.")
    return db

def create_car(db, brand, year, registration_number, max_payload, driver_id):
    """Добавление нового автомобиля в таблицу cars."""
    cars_collection = db["cars"]
    car_data = {
        "brand": brand,
        "year": year,
        "registration_number": registration_number,
        "max_payload": max_payload,
        "driver_id": driver_id
    }
    car_id = cars_collection.insert_one(car_data).inserted_id
    print(f"Автомобиль с идентификатором '{car_id}' добавлен успешно.")

def get_car_by_id(db, car_id):
    """Извлечение данных об автомобиле по его идентификатору."""
    cars_collection = db["cars"]
    car_data = cars_collection.find_one({"_id": car_id})
    if car_data:
        print(f"Идентификатор: {car_data['_id']}, Марка: {car_data['brand']}, "
              f"Год выпуска: {car_data['year']}, Гос. номер: {car_data['registration_number']}, "
              f"Максимальная грузоподъемность: {car_data['max_payload']}, ID водителя: {car_data['driver_id']}")
    else:
        print(f"Автомобиль с идентификатором '{car_id}' не найден.")

def update_car(db, car_id, new_data):
    """Обновление данных об автомобиле по его идентификатору."""
    cars_collection = db["cars"]
    updated_car = cars_collection.update_one({"_id": car_id}, {"$set": new_data})
    if updated_car.modified_count > 0:
        print(f"Данные об автомобиле с идентификатором '{car_id}' успешно обновлены.")
    else:
        print(f"Автомобиль с идентификатором '{car_id}' не найден.")

def delete_car(db, car_id):
    """Удаление автомобиля из таблицы cars по его идентификатору."""
    cars_collection = db["cars"]
    deleted_car = cars_collection.delete_one({"_id": car_id})
    if deleted_car.deleted_count > 0:
        print(f"Автомобиль с идентификатором '{car_id}' успешно удален.")
    else:
        print(f"Автомобиль с идентификатором '{car_id}' не найден.")

if __name__ == '__main__':
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description='Interact with MongoDB database for cars')
    parser.add_argument('csv_file', help='Path to the CSV file with car data')
    args = parser.parse_args()

    # Подключение к базе данных MongoDB
    db = connect_to_mongodb()

    # Чтение данных из CSV и добавление в базу данных
    with open(args.csv_file, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Пропускаем заголовки столбцов
        for row in csvreader:
            brand, year, reg_num, max_payload, driver_id = row
            year = int(year)
            max_payload = int(max_payload)
            create_car(db, brand, year, reg_num, max_payload, driver_id)

    '''
    # Примеры использования функций
    create_car(db, "Toyota", 2022, "AB1234", 1500, "driver123")
    car_id = "61432832ea6724ea60dc039c"  # Предполагаем, что этот идентификатор был возвращен при добавлении автомобиля
    get_car_by_id(db, car_id)
    update_data = {"max_payload": 1800, "driver_id": "driver456"}
    update_car(db, car_id, update_data)
    get_car_by_id(db, car_id)
    delete_car(db, car_id)
    '''

    # Закрытие соединения с базой данных
    db.client.close()
