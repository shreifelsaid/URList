from flask_login import LoginManager, UserMixin , login_user, logout_user, login_required
from app import db

class user(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key= True)
    email = db.Column(db.String(200), unique = True)
    username = db.Column(db.String(200), unique = True)
    password = db.Column(db.String(100))

class posts(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(500), nullable = False)
    body = db.Column(db.String(500), nullable = False)
    price = db.Column(db.String(500), nullable = False)
    pic = db.Column(db.String(500), nullable = False)
    # author_username = db.Column(db.String(500), nullable = False)
    # author_email = db.Column(db.String(500), nullable = False)
