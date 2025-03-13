import sqlite3

class Database:
    def __init__(self, db_path="database.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Создаёт таблицу пользователей, если её нет"""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            address TEXT,
            is_banned BOOLEAN DEFAULT 0
            
        )
        """)
        self.conn.commit()

    def add_user(self, user_id: int, first_name: str, address: str):
        """Добавляет пользователя в базу данных"""
        self.cursor.execute("INSERT OR IGNORE INTO users (user_id, first_name, address) VALUES (?, ?, ?)", 
                            (user_id, first_name, address))
        self.conn.commit()

    def get_user(self, user_id: int):
        """Получает данные пользователя"""
        self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()
    
    def delete_user(self, user_id: int):
        self.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        

    def ban_user(self, user_id: int):
        """Банит пользователя"""
        self.cursor.execute("UPDATE users SET is_banned = 1 WHERE user_id = ?", (user_id,))
        affected_rows = self.cursor.rowcount
        self.conn.commit()
        if affected_rows > 0:
            return True
        else:
            return False

    def unban_user(self, user_id: int):
        """Разбанит пользователя"""
        self.cursor.execute("UPDATE users SET is_banned = 0 WHERE user_id = ?", (user_id,))
        affected_rows = self.cursor.rowcount
        self.conn.commit()
        if affected_rows > 0:
            return True
        else:
            return False

    def close(self):
        """Закрывает соединение с БД"""
        self.conn.close()
