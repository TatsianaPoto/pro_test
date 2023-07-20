import sqlite3

def create_connection(database):
    """Создание или подключение к базе данных."""
    conn = None
    try:
        conn = sqlite3.connect(database)
        print("Подключение к базе данных успешно установлено.")
        return conn
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
    return conn

def create_table_cars(conn):
    """Создание таблицы 'cars' в базе данных."""
    sql = '''CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY,
                brand TEXT NOT NULL,
                year INTEGER NOT NULL,
                registration_number TEXT NOT NULL,
                max_payload REAL,
                driver_id INTEGER
            )'''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Таблица 'cars' успешно создана.")

def insert_car(conn, brand, year, registration_number, max_payload, driver_id):
    """Добавление данных об автомобиле в таблицу 'cars'."""
    sql = '''INSERT INTO cars (brand, year, registration_number, max_payload, driver_id)
             VALUES (?, ?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, (brand, year, registration_number, max_payload, driver_id))
    conn.commit()
    print("Данные об автомобиле успешно добавлены.")

def get_car_by_id(conn, car_id):
    """Извлечение данных об автомобиле по его идентификатору."""
    sql = '''SELECT * FROM cars WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (car_id,))
    row = cur.fetchone()
    return row

def update_car(conn, car_id, brand, year, registration_number, max_payload, driver_id):
    """Обновление данных об автомобиле."""
    sql = '''UPDATE cars SET brand=?, year=?, registration_number=?, max_payload=?, driver_id=?
             WHERE id=?'''
    cur = conn.cursor()
    cur.execute(sql, (brand, year, registration_number, max_payload, driver_id, car_id))
    conn.commit()
    print("Данные об автомобиле успешно обновлены.")

def delete_car(conn, car_id):
    """Удаление данных об автомобиле по его идентификатору."""
    sql = '''DELETE FROM cars WHERE id=?'''
    cur = conn.cursor()
    cur.execute(sql, (car_id,))
    conn.commit()
    print("Данные об автомобиле успешно удалены.")

if __name__ == '__main__':
    # Создание или подключение к базе данных
    database = 'transport.db'
    conn = create_connection(database)

    # Создание таблицы 'cars', если она не существует
    create_table_cars(conn)

    # Добавление данных об автомобиле
    insert_car(conn, 'Toyota', 2021, 'AB1234CD', 1500, 1)

    # Извлечение данных об автомобиле по идентификатору и вывод на экран
    car_id = 1
    car_data = get_car_by_id(conn, car_id)
    print("Данные об автомобиле с id:", car_id)
    print(car_data)

    # Обновление данных об автомобиле
    update_car(conn, car_id, 'Nissan', 2022, 'XY5678ZW', 1200, 2)

    # Извлечение данных обновленного автомобиля и вывод на экран
    updated_car_data = get_car_by_id(conn, car_id)
    print("Обновленные данные об автомобиле с id:", car_id)
    print(updated_car_data)

    # Удаление данных об автомобиле
    delete_car(conn, car_id)

    # Закрытие соединения с базой данных
    conn.close()
