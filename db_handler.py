import os
import sqlite3
from loguru import logger

base_path = os.path.join(os.path.dirname(__file__), 'sent_files.db')
logger.info(f'{base_path = }')


def initialize_database():
    """
    Создает базу данных и таблицу, если они не существуют.
     """

    # conn = sqlite3.connect('sent_files.db')
    conn = sqlite3.connect(base_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sent_files (
            filename TEXT,
            ftp_name TEXT,
            sent_date TEXT
        )
    ''')
    conn.commit()
    conn.close()


def log_file_sent(file_name, ftp_name):
    """
    Логирует отправку файла в базу данных.
    """
    # conn = sqlite3.connect('sent_files.db')
    conn = sqlite3.connect(base_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sent_files (filename, ftp_name, sent_date) VALUES (?, ?, datetime('now'))",
                   (file_name, ftp_name))
    conn.commit()
    conn.close()


def is_file_sent(file_name):
    """
    Проверяет, отправлялся ли файл ранее.
    """
    conn = sqlite3.connect(base_path)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM sent_files WHERE filename = ?", (file_name,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def read_data_from_db(base_path, query):
    # Подключение к базе данных SQLite
    conn = sqlite3.connect(base_path)
    cursor = conn.cursor()

    # Выполнение SQL-запроса
    cursor.execute(query)

    # Чтение всех строк результата запроса
    rows = cursor.fetchall()

    # Закрытие соединения
    conn.close()

    return rows


if __name__ == '__main__':
    initialize_database()

    _query = 'SELECT * FROM sent_files;'  # SQL-запрос для получения всех данных
    data = read_data_from_db(base_path, _query)
    for row in data:
        print(row)  # Выводим каждую строку результата
