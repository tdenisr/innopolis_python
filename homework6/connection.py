import sqlite3

DATABASE = 'test_stands.db'

def get_db():
    """Функция для получения соединения с базой данных."""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def get_db_cursor():
    """Функция для получения курсора базы данных"""
    with get_db() as db:
        cursor = db.cursor()
        return cursor
