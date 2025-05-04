CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    timestamp TEXT,
    user_id REFERENCES users
);

CREATE TABLE rec_classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    title TEXT,
    value TEXT
);

CREATE TABLE rating (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    user_id INTEGER REFERENCES users,
    rating INTEGER,
    comment TEXT
);
