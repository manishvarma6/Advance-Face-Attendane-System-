import sqlite3
import os
import pandas as pd
from datetime import datetime

DB_PATH = "backend/database/attendance.db"

EXPORT_DIR = "exports"


def export_today_attendance():

    today_date = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT user_id, date, time
        FROM attendance
        WHERE date = ?
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(today_date,)
    )

    conn.close()

    if df.empty:

        print("⚠️ No attendance today to export")
        return

    os.makedirs(EXPORT_DIR, exist_ok=True)

    file_name = f"attendance_{today_date}.xlsx"

    file_path = os.path.join(
        EXPORT_DIR,
        file_name
    )

    df.to_excel(
        file_path,
        index=False
    )

    print(f"📊 Excel Exported: {file_path}")