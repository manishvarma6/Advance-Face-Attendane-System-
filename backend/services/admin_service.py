import sqlite3

DB_PATH = "backend/database/attendance.db"

def validate_admin(username, password):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM admin
    WHERE username=? AND password=?
    """, (username, password))

    result = cursor.fetchone()

    conn.close()

    return result is not None

def change_password(username, old_password, new_password):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check old password
    cursor.execute("""
    SELECT * FROM admin
    WHERE username=? AND password=?
    """, (username, old_password))

    if not cursor.fetchone():
        conn.close()
        return False

    # Update new password
    cursor.execute("""
    UPDATE admin
    SET password=?
    WHERE username=?
    """, (new_password, username))

    conn.commit()
    conn.close()

    return True