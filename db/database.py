import sqlite3
from datetime import datetime

DB_NAME = "fitness_bot.db"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    with connect() as conn:
        cur = conn.cursor()
        # Таблица пользователей
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                tg_id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                gender TEXT,
                level TEXT,
                program_id TEXT,
                joined_at TEXT
            )
        """)
        # Таблица прогресса
        cur.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER,
                date TEXT,
                warmup_done INTEGER DEFAULT 0,
                cardio_done INTEGER DEFAULT 0,
                strength_done INTEGER DEFAULT 0,
                stretch_done INTEGER DEFAULT 0
            )
        """)
        conn.commit()

def add_user(tg_id, name, age, gender, level, program_id):
    with connect() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO users 
            (tg_id, name, age, gender, level, program_id, joined_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (tg_id, name, age, gender, level, program_id, datetime.now().isoformat()))
        conn.commit()

def get_user(tg_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
        return cur.fetchone()
