def get_today_summary():
    import sqlite3
    from datetime import date

    conn = sqlite3.connect("backend/database/attendance.db")
    cursor = conn.cursor()

    today = date.today().strftime("%Y-%m-%d")

    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM attendance WHERE date=?", (today,))
    present = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attendance WHERE user_id='Unknown' AND date=?", (today,))
    unknown = cursor.fetchone()[0]

    conn.close()

    return present, unknown