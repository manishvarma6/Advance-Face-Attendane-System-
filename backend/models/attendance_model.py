from backend.utils.database_utils import get_connection

def mark_attendance(user_id, date, time, confidence, image_path):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO attendance
        (user_id, date, time, confidence, image_path)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, date, time, confidence, image_path))

    conn.commit()
    conn.close()


def get_attendance_by_date(date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM attendance
        WHERE date=?
    """, (date,))

    records = cursor.fetchall()

    conn.close()

    return records