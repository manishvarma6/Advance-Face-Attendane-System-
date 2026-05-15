import sqlite3
from openpyxl import Workbook
from datetime import datetime
import os

DB_PATH = "backend/database/attendance.db"

EXPORT_DIR = "exports"


def export_attendance_to_excel():

    # Create export folder
    os.makedirs(EXPORT_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get attendance data
    cursor.execute("""
        SELECT 
            user_id,
            department,
            date,
            time,
            confidence,
            status
        FROM attendance
        ORDER BY date DESC
    """)

    records = cursor.fetchall()

    conn.close()

    if len(records) == 0:
        print("⚠️ No attendance data found")
        return

    # Create Excel workbook
    wb = Workbook()
    ws = wb.active

    ws.title = "Attendance Report"

    # Header Row
    headers = [
        "User ID",
        "Department",
        "Date",
        "Time",
        "Confidence",
        "Status"
    ]

    ws.append(headers)

    # Add Data
    for row in records:
        ws.append(row)

    # Save file
    today_date = datetime.now().strftime("%Y-%m-%d")

    file_name = f"Attendance_{today_date}.xlsx"

    file_path = os.path.join(
        EXPORT_DIR,
        file_name
    )

    wb.save(file_path)

    print(f"✅ Excel Exported: {file_path}")