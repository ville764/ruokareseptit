import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM items")
db.execute("DELETE FROM classes")
db.execute("DELETE FROM rating")
db.execute("CREATE INDEX idx_items_id ON items (id DESC);")
db.execute("CREATE INDEX idx_rating_item_id ON rating (item_id);")


user_count = 1000
item_count = 10**6
rating_count = 10**7


rec_classes = db.execute("SELECT title, value FROM rec_classes").fetchall()


for i in range(1, user_count + 1):
    username = f"user{i}"
    password_hash = "hashedpassword"  
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))

for i in range(1, item_count + 1):
    title = f"Recipe {i}"
    description = f"This is the description for recipe {i}."
    timestamp = "2025-04-26 12:00:00"
    user_id = random.randint(1, user_count)
    db.execute("""INSERT INTO items (title, description, timestamp, user_id) 
                  VALUES (?, ?, ?, ?)""", (title, description, timestamp, user_id))


for item_id in range(1, item_count + 1):
    for _ in range(random.randint(1, 3)):  
        title, value = random.choice(rec_classes)
        db.execute("INSERT INTO classes (item_id, title, value) VALUES (?, ?, ?)", (item_id, title, value))


for i in range(1, rating_count + 1):
    item_id = random.randint(1, item_count)
    user_id = random.randint(1, user_count)
    rating_value = random.randint(1, 5)
    comment = f"Comment {i}"
    db.execute("""INSERT INTO rating (item_id, user_id, rating, comment) 
                  VALUES (?, ?, ?, ?)""", (item_id, user_id, rating_value, comment))

db.commit()
db.close()
