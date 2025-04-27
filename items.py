import db

def get_all_res_classes():
    sql = """SELECT title, value
    FROM rec_classes ORDER BY id"""
    result = db.query(sql)
    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)
    return classes

def add_item(title, description, user_id, classes):
    sql = "INSERT INTO items (title, description, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, description, user_id])
    item_id = db.last_insert_id()

    sql = "INSERT INTO classes (item_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [item_id, class_title, class_value])

def add_rating(rating, user_id, item_id, comment):
    sql = "INSERT INTO rating (rating, user_id, item_id, comment) VALUES (?, ?, ?, ?)"
    db.execute(sql, [rating, user_id, item_id, comment])

def get_rating_avg(item_id):
    sql = "SELECT AVG(rating) FROM rating WHERE item_id = ?"
    result = db.query(sql, [item_id])
    if result and result[0][0] is not None:
        return round(result[0][0], 2)
    return None

def get_rating_count(item_id):
    sql = "SELECT count(rating) FROM rating WHERE item_id = ?"
    result = db.query(sql, [item_id])
    if result and result[0][0] is not None:
        return result[0][0]
    return None

def get_comments(item_id):
    sql = "SELECT comment FROM rating WHERE item_id = ? ORDER BY id DESC"
    result = db.query(sql, [item_id])
    if result:
        return result
    return None

def get_classes(item_id):
    sql = """SELECT title, value
    FROM classes
    WHERE classes.item_id = ?"""
    result = db.query(sql, [item_id])
    return result

def get_items(page=1, page_size=10):
    offset = (page - 1) * page_size
    sql = "SELECT id, title, description, user_id FROM items ORDER BY id DESC LIMIT ? OFFSET ?"
    return db.query(sql, [page_size, offset])


def item_count():
    sql = "SELECT COUNT(*) FROM items"
    result = db.query(sql)
    return result[0][0]

def get_item(item_id):
    sql = """SELECT items.id, items.title, items.description, users.username, users.id user_id
    FROM items, users 
    WHERE items.user_id = users.id 
    AND items.id = ?"""
    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, title, description, classes):
    sql = "UPDATE items SET title = ?, description = ? WHERE id = ?"
    db.execute(sql, [title, description, item_id])

    sql = "DELETE FROM classes WHERE item_id = ?"
    db.execute(sql, [item_id])

    sql = "INSERT INTO classes (item_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [item_id, class_title, class_value])

def remove_item(item_id):
    sql = "DELETE FROM classes WHERE item_id = ?"
    db.execute(sql, [item_id])
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql = """SELECT items.id, items.title
    FROM items
    WHERE items.description LIKE ? OR items.title LIKE ?
    ORDER BY items.id DESC"""
    like_query = "%" + query + "%"
    return db.query(sql, [like_query, like_query])
