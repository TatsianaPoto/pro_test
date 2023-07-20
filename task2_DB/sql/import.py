import argparse
import csv
import sqlite3

def create_connection(database):
    conn = None
    try:
        conn = sqlite3.connect(database)
        print("Connection to SQLite database successful")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred while connecting to the database")
    return conn

def create_table_cars(conn):
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY,
        brand TEXT NOT NULL,
        year INTEGER NOT NULL,
        registration_number TEXT NOT NULL,
        max_payload REAL NOT NULL,
        driver_id INTEGER NOT NULL
    );
    """
    try:
        c = conn.cursor()
        c.execute(sql_create_table)
        print("Table 'cars' created successfully")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred while creating the table")

def insert_car(conn, brand, year, registration_number, max_payload, driver_id):
    sql_insert_car = """
    INSERT INTO cars (brand, year, registration_number, max_payload, driver_id)
    VALUES (?, ?, ?, ?, ?)
    """
    try:
        c = conn.cursor()
        c.execute(sql_insert_car, (brand, year, registration_number, max_payload, driver_id))
        conn.commit()
        print("Car inserted successfully")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred while inserting a car")

def get_car_by_id(conn, car_id):
    sql_select_car = """
    SELECT * FROM cars WHERE id = ?
    """
    try:
        c = conn.cursor()
        c.execute(sql_select_car, (car_id,))
        car_data = c.fetchone()
        if car_data:
            return car_data
        else:
            print(f"Car with id {car_id} not found")
            return None
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred while fetching a car")

def update_car(conn, car_id, brand, year, registration_number, max_payload, driver_id):
    sql_update_car = """
    UPDATE cars
    SET brand = ?, year = ?, registration_number = ?, max_payload = ?, driver_id = ?
    WHERE id = ?
    """
    try:
        c = conn.cursor()
        c.execute(sql_update_car, (brand, year, registration_number, max_payload, driver_id, car_id))
        conn.commit()
        print(f"Car with id {car_id} updated successfully")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred while updating a car")

def delete_car(conn, car_id):
    sql_delete_car = """
    DELETE FROM cars WHERE id = ?
    """
    try:
        c = conn.cursor()
        c.execute(sql_delete_car, (car_id,))
        conn.commit()
        print(f"Car with id {car_id} deleted successfully")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred while deleting a car")

def read_csv_file(file_path):
    cars_data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cars_data.append(row)
    return cars_data

def main(database, csv_file):
    conn = create_connection(database)
    create_table_cars(conn)

    cars_data = read_csv_file(csv_file)
    for car in cars_data:
        insert_car(conn, car['brand'], int(car['year']), car['registration_number'],
                   float(car['max_payload']), int(car['driver_id']))

    # Примеры работы с данными (извлечение, обновление, удаление)
    car_id = 1
    car_data = get_car_by_id(conn, car_id)
    print("Данные об автомобиле с id:", car_id)
    print(car_data)

    update_car(conn, car_id, 'Nissan', 2022, 'XY5678ZW', 1200, 2)

    updated_car_data = get_car_by_id(conn, car_id)
    print("Обновленные данные об автомобиле с id:", car_id)
    print(updated_car_data)

    delete_car(conn, car_id)

    conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Заполнение таблицы cars данными из CSV-файла.')
    parser.add_argument('database', help='Имя файла базы данных')
    parser.add_argument('csv_file', help='Путь к CSV-файлу с данными для заполнения таблицы cars')
    args = parser.parse_args()

    main(args.database, args.csv_file)
