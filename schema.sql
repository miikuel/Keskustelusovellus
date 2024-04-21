CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin BOOLEAN NOT NULL DEFAULT false,
    registered_at TIMESTAMP
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    secret BOOLEAN NOT NULL,
    created_by INTEGER REFERENCES users,
    created_at TIMESTAMP
);

CREATE TABLE topic_permissions (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    topic_id INTEGER REFERENCES topics ON DELETE CASCADE,
    created_by INTEGER REFERENCES users,
    created_at TIMESTAMP,
    edited BOOLEAN DEFAULT false
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    message TEXT,
    created_by INTEGER REFERENCES users,
    thread_id INTEGER REFERENCES threads ON DELETE CASCADE,
    topic_id INTEGER REFERENCES topics ON DELETE CASCADE,
    created_at TIMESTAMP,
    edited_at TIMESTAMP,
    edited BOOLEAN DEFAULT false,
    deleted BOOLEAN DEFAULT false
);