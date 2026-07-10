import sqlite3
from data import models

DATA = "data/users_db.db"
def get_user_by_pass_mail(email, password):
    conn = sqlite3.connect(DATA)
    c = conn.cursor()
    c.execute("""SELECT
            user_id,
            is_admin,
            user_name,
            user_role,
            user_phone,
            user_email,
            user_pass,
            user_reg_by,
            user_img,
            user_theme
            FROM users
            WHERE user_email = ? AND user_pass = ?""",(email, password))
    row = c.fetchone()
    conn.close()
    if row:
        return models.User(*row)
    return None

def get_users_email():
    conn = sqlite3.connect(DATA)
    c = conn.cursor()
    c.execute("""SELECT user_email FROM users""")
    row = c.fetchall()
    return row
    

def get_mail_exists(email):
    conn = sqlite3.connect(DATA)
    c = conn.cursor()
    c.execute("""
            SELECT * FROM users WHERE user_email = ?
            """, (email,))
    result = c.fetchone()
    conn.close()
    return result

def update_user_pass(user_pass, user_email):
    conn = sqlite3.connect(DATA)
    c = conn.cursor()
    c.execute("""
            UPDATE users
            SET user_pass = ?
            WHERE user_email = ?
            """, (user_pass, user_email),)
    conn.commit()
    conn.close()

def update_user_theme(user_theme, user_email):
    conn = sqlite3.connect(DATA)
    c = conn.cursor()
    c.execute("""
              UPDATE users
              SET user_theme = ?
              WHERE user_email = ?
              """, (user_theme, user_email),)
    conn.commit()
    conn.close()

def update_user(user_data):
    conn = sqlite3.connect(DATA)
    c = conn.cursor()
    c.execute("""
            UPDATE users SET
            is_admin = ?,
            user_name = ?,
            user_role = ?,
            user_phone = ?,
            user_email = ?,
            user_img = ?,
            user_theme = ?
            WHERE user_id = ?
            """, (
            user_data[1], # is_admin
            user_data[2], # user_name
            user_data[3], # user_role
            user_data[4], # user_phone
            user_data[5], # user_email
            user_data[8], # user_img
            user_data[9], # user_theme
            user_data[0]  # user_id
            ),)
    conn.commit()
    conn.close()


def insert_new_user(is_admin, user_name, user_role, user_phone, user_email, reg_by, user_img, user_theme):
    conn = sqlite3.connect(DATA)
    c = conn.cursor()
    c.execute("""
            INSERT INTO users(
                        is_admin,
                        user_name,
                        user_role,
                        user_phone,
                        user_email,
                        user_pass,
                        user_reg_by,
                        user_img,
                        user_theme)
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,(is_admin, user_name, user_role, user_phone, user_email, "__Temp__", reg_by, user_img, user_theme
            ))
    conn.commit()
    conn.close()

def delete_by_email(delete_mail):
    conn = sqlite3.connect(DATA)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE user_email = ?", (delete_mail,))
    conn.commit()
    conn.close()