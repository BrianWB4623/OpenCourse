from app import db 
from app import login_manager
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(128))  # can keep plain for now
    email = db.Column(db.String(100), nullable=False, unique=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(120), nullable=False)

