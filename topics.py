from db import db
from flask import session
from sqlalchemy.sql import text
from datetime import datetime

def new_topic(topic_name):
    sql = "SELECT id, admin FROM users where username=:username"
    result = db.session.execute(text(sql), {"username":session["username"]})
    user = result.fetchone()
    if not user.admin:
        return False
    try:
        sql = "INSERT INTO topics (name, created_by, created_at) VALUES (:name, :created_by, :date)"
        db.session.execute(text(sql), {"name":topic_name.capitalize(), "created_by":user.id, "date":datetime.now().replace(microsecond=0)})
        db.session.commit()
        return True
    except:
        return False
    
def get_topics():
    sql = "SELECT name FROM topics ORDER BY name"
    result = db.session.execute(text(sql))
    names = result.fetchall()
    return names

def thread_creator(threadname):
    sql = "SELECT t.name, u.username FROM threads t, users u WHERE u.id=t.created_by AND LOWER(t.name)=:name AND u.username=:username"
    result = db.session.execute(text(sql), {"name":threadname, "username":session["username"]})
    creator = result.fetchone()
    if creator:
        return True
    return False

def message_author(id):
    sql = "SELECT username FROM users u, messages m WHERE u.id=m.created_by AND m.id=:id AND username=:username"
    result = db.session.execute(text(sql), {"id":id, "username":session["username"]})
    username = result.fetchone()
    if username:
        return True
    else:
        return False


def topic_threads(topic):
    sql = "SELECT id FROM topics WHERE LOWER(name)=:topic"
    result = db.session.execute(text(sql), {"topic":topic})
    topic_id = result.fetchone()[0]
    sql = "SELECT t.name, COUNT(m.*) messages, MAX(m.created_at) latest FROM threads t, messages m WHERE t.id=m.thread_id AND t.topic_id=:topic_id GROUP BY t.name"
    result = db.session.execute(text(sql), {"topic_id":topic_id})
    threads = result.fetchall()
    return threads

def get_messages(thread):
    sql = "SELECT id FROM threads WHERE name=:name"
    result = db.session.execute(text(sql), {"name":thread.capitalize()})
    thread_id = result.fetchone()[0]
    sql = "SELECT ROW_NUMBER() OVER (ORDER BY m.created_at) AS rownumber, m.message, u.username, m.created_at, m.id, m.deleted FROM messages m, users u WHERE u.id=m.created_by AND thread_id=:thread_id ORDER BY m.created_at"
    result =  db.session.execute(text(sql), {"thread_id":thread_id})
    messages = result.fetchall()
    return messages

def new_thread(topicname, threadname, content):
    try:
        sql = "SELECT id FROM topics WHERE name=:name"
        result = db.session.execute(text(sql), {"name":topicname.capitalize()})
        topic_id = result.fetchone()[0]
        sql = "SELECT id FROM users WHERE username=:username"
        result = db.session.execute(text(sql), {"username":session["username"]})
        user_id = result.fetchone()[0]
        sql = "INSERT INTO threads (name, topic_id, created_by, created_at) VALUES (:threadname, :topic_id, :user_id, :created_at) RETURNING id"
        result = db.session.execute(text(sql), {"threadname":threadname.capitalize(), "topic_id":topic_id, "user_id":user_id, "created_at":datetime.now().replace(microsecond=0)})
        thread_id = result.fetchone()[0]
        sql = "INSERT INTO messages (message, created_by, thread_id, topic_id, created_at) VALUES (:message, :user_id, :thread_id, :topic_id, :created_at)"
        db.session.execute(text(sql), {"message":content, "user_id":user_id, "thread_id":thread_id, "topic_id":topic_id, "created_at":datetime.now().replace(microsecond=0)})
        db.session.commit()
        return True
    except:
        return False
    

def new_message(thread, message):
    try:
        sql = "SELECT id, topic_id FROM threads WHERE name=:name"
        result = db.session.execute(text(sql), {"name":thread.capitalize()})
        ids = result.fetchone()
        thread_id = ids[0]
        topic_id = ids[1]
        sql = "SELECT id FROM users WHERE username=:username"
        result = db.session.execute(text(sql), {"username":session["username"]})
        user_id = result.fetchone()[0]
        sql = "INSERT INTO messages (message, created_by, thread_id, topic_id, created_at) VALUES (:message, :user_id, :thread_id, :topic_id, :created_at)"
        db.session.execute(text(sql), {"message":message, "user_id":user_id, "thread_id":thread_id, "topic_id":topic_id, "created_at":datetime.now().replace(microsecond=0)})
        db.session.commit()
        return True
    except:
        return False
    

def search_messages(query):
    sql = "SELECT m.message, m.created_at, m.edited, m.created_by, users.username, topics.name topicname, threads.name threadname FROM messages m, topics, threads, users WHERE topics.id=m.topic_id AND threads.id=m.thread_id AND users.id=m.created_by AND LOWER(m.message) LIKE :query"
    result = db.session.execute(text(sql), {"query":"%"+query.lower()+"%"})
    messages = result.fetchall()
    return messages

def delete_topic(name):
    try:
        sql = "DELETE FROM topics WHERE name=:name"
        db.session.execute(text(sql), {"name":name})
        db.session.commit()
        return True
    except:
        return False
    
def rename_thread(name, newname):
    try:
        sql = "UPDATE threads SET name=:newname WHERE LOWER(name)=:name"
        db.session.execute(text(sql), {"newname":newname, "name":name.lower()})
        db.session.commit()
        return True
    except:
        return False

def delete_thread(name):
    try:
        sql = "DELETE FROM threads WHERE LOWER(name)=:name"
        db.session.execute(text(sql), {"name":name.lower()})
        db.session.commit()
        return True
    except:
        return False
    
def delete_message(id, admin):
    try:
        if admin:
            msg = "Ylläpitäjä on poistanut viestin"
        else:
            msg = "Käyttäjä on poistanut viestin"
        sql = "UPDATE messages SET message=:message WHERE id=:id"
        db.session.execute(text(sql), {"message":msg, "id":id})
        sql = "UPDATE messages SET deleted = TRUE WHERE id=:id"
        db.session.execute(text(sql), {"id":id})
        db.session.commit()
        return True
    except:
        return False