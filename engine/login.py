import sqlite3

from engine.paths import DB_PATH

DB_NAME = DB_PATH


def create_user_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()

    


def login_user(email, password):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cur.fetchone()

    conn.close()

    if user:
        return True

    return False
 

def register_user(first_name, last_name, phone, email, password):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:

        cur.execute("""
            INSERT INTO users
            (first_name,last_name,phone,email,password)
            VALUES(?,?,?,?,?)
        """,
        (first_name, last_name, phone, email, password))

        conn.commit()
        conn.close()

        return True

    except sqlite3.IntegrityError:

        conn.close()
        return False










    # ===== NEW FUNCTION =====

def check_email(email):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    user = cur.fetchone()

    conn.close()

    if user:
        return True

    return False

def update_password(email, new_password):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET password=? WHERE email=?",
        (new_password, email)
    )

    conn.commit()

    conn.close()

    return True




def update_users_table():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    columns = [
        ("first_name", "TEXT"),
        ("last_name", "TEXT"),
        ("phone", "TEXT")
    ]

    for column_name, column_type in columns:
        try:
            cur.execute(
                f"ALTER TABLE users ADD COLUMN {column_name} {column_type}"
            )
        except sqlite3.OperationalError:
            # Column already exists
            pass

    conn.commit()
    conn.close()