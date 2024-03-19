from db import db
from flask import session
from sqlalchemy.sql import text

def new_topic(topic_name):
    sql = "SELECT id, admin FROM users where username=:username"
    result = db.session.execute(text(sql), {"username":session["username"]})
    user = result.fetchone()
    if not user.admin:
        return False
    try:
        sql = "INSERT INTO topics (name, created_by) VALUES (:name, :created_by)"
        db.session.execute(text(sql), {"name":topic_name.capitalize(), "created_by":user.id})
        db.session.commit()
        return True
    except:
        return False
    
def get_topics():
    sql = "SELECT name FROM topics"
    result = db.session.execute(text(sql))
    names = result.fetchall()
    return names