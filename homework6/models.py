from connection import get_db

def init_db():
    """Инициализация базы данных с созданием необходимых таблиц."""
    with get_db() as db:
        cursor = db.cursor()
        # Создание таблицы Users
        cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            last_name TEXT NOT NULL,
                            first_name TEXT NOT NULL,
                            comments TEXT
                        );''')

        # Создание таблицы Stands
        cursor.execute('''CREATE TABLE IF NOT EXISTS Stands (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            ip_address TEXT NOT NULL,
                            operating_system TEXT NOT NULL,
                            os_version TEXT NOT NULL,
                            stand_type TEXT NOT NULL,
                            cpu_count INTEGER NOT NULL,
                            memory_size INTEGER NOT NULL,
                            comments TEXT
                        );''')

        # Создание таблицы Bookings
        cursor.execute('''CREATE TABLE IF NOT EXISTS Bookings (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            stand_id INTEGER NOT NULL,
                            user_id INTEGER NOT NULL,
                            start_time DATETIME NOT NULL,
                            end_time DATETIME,
                            completed BOOLEAN NOT NULL DEFAULT 0,
                            comments TEXT,
                            FOREIGN KEY (stand_id) REFERENCES Stands(id),
                            FOREIGN KEY (user_id) REFERENCES Users(id)
                        );''')

        db.commit()