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

if __name__ == '__main__':
    # Создание или подключение к базе данных
    database = 'transport.db'
    conn = create_connection(database)

    # Создание таблицы 'cars'
    create_table_cars(conn)

    # Закрытие соединения с базой данных
    conn.close()
