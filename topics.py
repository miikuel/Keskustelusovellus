from db import db
from flask import session
from sqlalchemy.sql import text

def new_section(section_name):
    sql = "SELECT id, admin FROM users where username=:username"
    result = db.session.execute(text(sql), {"username":session["username"]})
    user = result.fetchone()
    if not user.admin:
        return False
    try:
        sql = "INSERT INTO sections (name, created_by) VALUES (:name, :created_by)"
        db.session.execute(text(sql), {"name":section_name.capitalize(), "created_by":user.id})
        db.session.commit()
        return True
    except:
        return False
    
def get_sections():
    sql = "SELECT name FROM sections"
    result = db.session.execute(text(sql))
    names = result.fetchall()
    return names