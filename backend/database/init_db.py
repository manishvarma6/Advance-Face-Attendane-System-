import sqlite3
import os

DB_PATH = "backend/database/attendance.db"

def init_database():
    # Create database folder if not exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT UNIQUE,
        name TEXT NOT NULL,
        department TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create Attendance Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        date TEXT,
        department TEXT,
        time TEXT,
        confidence REAL,
        image_path TEXT,
        status TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    
    """)


    # Create Admin Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)


    conn.commit()
    conn.close()

    print("✅ Database Initialized Successfully")
    


if __name__ == "__main__":
    init_database()