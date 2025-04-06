import db

def add_item(title, description, user_id): 
    sql = "INSERT INTO items (title, description, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, description, user_id])

def get_items():
    sql = "SELECT * FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.id, items.title, items.description, users.username, users.id user_id
    FROM items, users 
    WHERE items.user_id = users.id 
    AND items.id = ?"""
    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, title, description):
    sql = "UPDATE items SET title = ?, description = ? WHERE id = ?"
    db.execute(sql, [title, description, item_id])

def remove_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql = """SELECT items.id, items.title
    FROM items
    WHERE items.description LIKE ? OR items.title LIKE ?
    ORDER BY items.id DESC"""
    like_query = "%" + query + "%"
    return db.query(sql, [like_query, like_query])
