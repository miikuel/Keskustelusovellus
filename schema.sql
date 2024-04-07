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
    created_by INTEGER REFERENCES users,
    created_at TIMESTAMP
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    topic_id INTEGER REFERENCES topics,
    created_by INTEGER REFERENCES users,
    created_at TIMESTAMP,
    edited BOOLEAN DEFAULT false
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    message TEXT,
    created_by INTEGER REFERENCES users,
    thread_id INTEGER REFERENCES threads,
    topic_id INTEGER REFERENCES topics,
    created_at TIMESTAMP,
    edited BOOLEAN DEFAULT false
);