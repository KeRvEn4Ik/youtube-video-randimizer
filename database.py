import sqlite3

def get_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row 
    return conn

def init_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL UNIQUE,
            user_password TEXT NOT NULL,
            theme INTEGER NOT NULL DEFAULT 0 
        )
    """)

    cursor.execute("""        
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            url_for_video TEXT NOT NULL,
            title TEXT NOT NULL)
    """)
    conn.commit()
    conn.close()

def get_one_user(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users_info WHERE user_name = ?', (name,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_user(name, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO users_info (user_name, user_password)
                   VALUES (?, ?)
                   """, (name, password))
    conn.commit()
    conn.close()

def check_user(name, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM users_info WHERE user_name = ? AND user_password = ?""", (name, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def check_user_login(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM users_info WHERE user_name = ?""", (name,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def update_theme(theme, name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""UPDATE users_info SET theme = ?
                   WHERE user_name = ?""", (theme, name))
    conn.commit()
    conn.close()

def delete_user_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users_info WHERE id = ?", (id,))
    conn.commit()
    conn.close()


def add_video(name, id, title):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO history (user_name, url_for_video, title)
                   VALUES (?, ?, ?)
                   """, (name, id, title))
    conn.commit()
    conn.close()

def get_history(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM history WHERE user_name = ?""", (name,))
    hitory = cursor.fetchall()
    conn.close()
    return hitory or []

