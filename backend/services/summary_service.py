import sqlite3
import os
from datetime import datetime

DB_PATH = "backend/database/attendance.db"

UNKNOWN_DIR = "face_data/unknown_faces"


def show_daily_summary():

    today_date = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Count Present Users
    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE date = ?
    """, (today_date,))

    present_count = cursor.fetchone()[0]

    conn.close()

    # Count Unknown Faces
    unknown_count = 0

    if os.path.exists(UNKNOWN_DIR):

        files = os.listdir(UNKNOWN_DIR)

        today_files = [
            f for f in files
            if today_date in f
        ]

        unknown_count = len(today_files)

    total_records = present_count + unknown_count

    print("\n📊 Today's Attendance Summary\n")

    print(f"✅ Total Present: {present_count}")

    print(f"🚨 Unknown Faces: {unknown_count}")

    print(f"📋 Total Records Today: {total_records}")