import sqlite3
import os


DB_PATH = "data/clinical.db"


def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS patient_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        name TEXT,
        mobile TEXT,
        language TEXT,

        gender TEXT,
        age INTEGER,
        hypertension INTEGER,
        heart_disease INTEGER,
        smoking_history TEXT,

        bmi REAL,
        hba1c REAL,
        glucose REAL,

        risk_probability REAL,
        risk_category TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
