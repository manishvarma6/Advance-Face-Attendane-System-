import sqlite3
from datetime import datetime
import os
import cv2

DB_PATH = "backend/database/attendance.db"

# Folder to save attendance images
ATTENDANCE_IMG_DIR = "face_data/attendance_logs"


def mark_attendance(user_id, confidence, frame):

    # Create folder if not exists
    os.makedirs(ATTENDANCE_IMG_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now()

    date_today = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H-%M-%S")

    # Get user department
    cursor.execute("""
        SELECT name, department
        FROM users
        WHERE user_id=?
    """, (user_id,))

    user = cursor.fetchone()

    if user is None:
        print("❌ User not found in database")
        conn.close()
        return

    name, department = user

    # Check duplicate attendance
    cursor.execute("""
        SELECT *
        FROM attendance
        WHERE user_id=? AND date=?
    """, (user_id, date_today))

    result = cursor.fetchone()

    if result is None:

        # Save attendance image
        image_name = f"{user_id}_{current_time}.jpg"
        image_path = os.path.join(
            ATTENDANCE_IMG_DIR,
            image_name
        )

        cv2.imwrite(image_path, frame)

        # Insert attendance
        cursor.execute("""
            INSERT INTO attendance
            (
                user_id,
                date,
                department,
                time,
                confidence,
                image_path,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            date_today,
            department,
            current_time,
            float(confidence),
            image_path,
            "Present"
        ))

        conn.commit()

        print(f"✅ Attendance Marked: {name} ({department})")

    else:

        print(f"⚠️ Already Marked Today: {name}")

    conn.close()