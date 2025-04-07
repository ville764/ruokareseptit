import db
from werkzeug.security import generate_password_hash, check_password_hash

def get_user(user_id):
    sql = """SELECT id, username
    FROM users 
    WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_items(user_id):
    sql = """SELECT id, title
    FROM items 
    WHERE user_id = ?
    ORDER BY id DESC""" 
    result = db.query(sql, [user_id])
    return result

def create_user(username, password1):
    password_hash = generate_password_hash(password1)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])  
        if not result:
            return None

        user = result[0]
        user_id = user["id"]
        password_hash = user["password_hash"]
        if check_password_hash(password_hash, password):
            return user_id
        else:
            return None
