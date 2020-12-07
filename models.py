from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class user(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key= True)
    email = db.Column(db.String(200), unique = True)
    username = db.Column(db.String(200), unique = True)
    password = db.Column(db.String(100))
    security_question = db.Column(db.Integer)
    security_answer = db.Column(db.String(500))

class posts(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(500), nullable = False)
    body = db.Column(db.String(500), nullable = False)
    price = db.Column(db.String(500), nullable = False)
    pic = db.Column(db.String(500), nullable = False)
    author_username = db.Column(db.String(500), nullable = False)
    author_email = db.Column(db.String(500), nullable = False)

class items(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    post_id = db.Column(db.Integer)
    email = db.Column(db.String(500))
