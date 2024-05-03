from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
import secrets

def login(username, password):
    sql = "SELECT id, password, admin FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["username"] = username
            session["user_id"] = user.id
            session["admin"] = user.admin
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False
        
def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, registered_at) VALUES (:username, :password, NOW()) RETURNING id"
        result = db.session.execute(text(sql), {"username":username, "password":hash_value})
        id = result.fetchone()[0]
        if id == 1:
            sql = "UPDATE users SET admin=TRUE WHERE id=1"
            db.session.execute(text(sql))
            db.session.commit()
            return True
        sql = "SELECT id from topics WHERE secret=FALSE"
        result = db.session.execute(text(sql))
        topic_ids = result.fetchall()
        for topic_id in topic_ids:
            sql = "INSERT INTO topic_permissions (topic_id, user_id) VALUES (:topic_id, :id)"
            db.session.execute(text(sql), {"topic_id":topic_id[0], "id":id})
        db.session.commit()
        return True
    except:
        return False

def logout():
    del session["username"]
    del session["user_id"]
    del session["admin"]
    del session["csrf_token"]

def is_admin():
    return session["admin"]

def is_logged():
    return session.get("username", 0)
