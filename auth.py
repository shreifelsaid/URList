from flask.helpers import flash
import app
from flask import Blueprint, render_template, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    login_form = app.LoginForm()
    return  render_template('login.html',login_form=login_form)

@auth.route('/logout')
def logout():
    return redirect(url_for('index')) 

@auth.route('/signup')
def signup():
    signup_form = app.SignupForm()
    return  render_template('signup.html',signup_form=signup_form)

@auth.route('/login', methods=['POST'])
def login_post():
    email = password = username = None
    login_form = app.LoginForm()
    if login_form.validate_on_submit():
        print("validated succcessfully")
        email = login_form.email.data
        username = login_form.email.data
        password = login_form.password.data
        user = app.user.query.filter((email == email) | (username == username)).first()
        if not user or not check_password_hash(user.password, password):
            flash("wrong password or username")
            return redirect(url_for('auth.login'))
        app.login_user(user)
    return redirect(url_for('index')) 

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = username = password   = None
    signup_form = app.SignupForm()
    if signup_form.validate_on_submit():
        print("validated succcessfully")
        email = signup_form.email.data
        username = signup_form.username.data
        password = signup_form.password.data
        user = app.user.query.filter((email == email) | (username == username)).first()
        if user :
            flash("Username or email is already in use, log in!")
            return redirect(url_for('auth.login'))
        db_entry = app.user(email=email, username=username, password=generate_password_hash(password, method='sha256'))
        try:
            app.db.session.add(db_entry)
            app.db.session.commit()
        except:
            return "Database error"
    return render_template('welcome.html', username=username)

# @auth.route('/welcome')
# def welcome():
#     return  render_template('welcome.html')