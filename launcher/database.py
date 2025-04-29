import sqlite3
from typing import Optional, Tuple

class Database:
    def __init__(self, db_name: str = "launcher.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        # Таблица пользователей
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            last_login TEXT
        )
        """)
        
        # Таблица настроек
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            java_path TEXT,
            memory_alloc INTEGER,
            resolution TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)
        
        self.conn.commit()

    def add_user(self, username: str, password: str) -> bool:
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def check_user(self, username: str, password: str) -> bool:
        self.cursor.execute(
            "SELECT 1 FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        return self.cursor.fetchone() is not None

    def get_user_settings(self, username: str) -> Optional[dict]:
        self.cursor.execute("""
        SELECT s.java_path, s.memory_alloc, s.resolution 
        FROM settings s
        JOIN users u ON s.user_id = u.id
        WHERE u.username = ?
        """, (username,))
        
        result = self.cursor.fetchone()
        if result:
            return {
                "java_path": result[0],
                "memory_alloc": result[1],
                "resolution": result[2]
            }
        return None

    def update_user_settings(self, username: str, settings: dict) -> bool:
        # Сначала получаем user_id
        self.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        
        if not user:
            return False
            
        user_id = user[0]
        
        # Проверяем, есть ли уже настройки для этого пользователя
        self.cursor.execute("SELECT 1 FROM settings WHERE user_id = ?", (user_id,))
        exists = self.cursor.fetchone()
        
        if exists:
            # Обновляем существующие настройки
            self.cursor.execute("""
            UPDATE settings SET
                java_path = ?,
                memory_alloc = ?,
                resolution = ?
            WHERE user_id = ?
            """, (
                settings.get("java_path"),
                settings.get("memory_alloc"),
                settings.get("resolution"),
                user_id
            ))
        else:
            # Добавляем новые настройки
            self.cursor.execute("""
            INSERT INTO settings (user_id, java_path, memory_alloc, resolution)
            VALUES (?, ?, ?, ?)
            """, (
                user_id,
                settings.get("java_path"),
                settings.get("memory_alloc"),
                settings.get("resolution")
            ))
        
        self.conn.commit()
        return True

    def close(self):
        self.conn.close()



