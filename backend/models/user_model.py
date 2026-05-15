from backend.utils.database_utils import get_connection

def add_user(user_id, name, department):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (user_id, name, department)
        VALUES (?, ?, ?)
    """, (user_id, name, department))

    conn.commit()
    conn.close()


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    users = cursor.fetchall()

    conn.close()

    return users


def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users WHERE user_id=?
    """, (user_id,))

    user = cursor.fetchone()

    conn.close()

    return user