from flask.helpers import flash
from flask_login import  login_user, logout_user, login_required, current_user
from models import user, db
from forms import LoginForm, SignupForm
from flask import Blueprint, render_template, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    login_form = LoginForm()
    return  render_template('login.html',login_form=login_form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 

@auth.route('/signup')
def signup():
    signup_form = SignupForm()
    return  render_template('signup.html',signup_form=signup_form)

@auth.route('/login', methods=['POST'])
def login_post():
    email = password = username = None
    login_form = LoginForm()
    if login_form.validate_on_submit():
        print("validated succcessfully")
        email = login_form.email.data
        username = login_form.email.data
        password = login_form.password.data
        existing_user = user.query.filter((email == user.email) | (username == user.username)).first()
        if not existing_user or not check_password_hash(existing_user.password, password):
            flash("wrong password or username")
            return redirect(url_for('auth.login'))
        login_user(existing_user)
    return redirect(url_for('index')) 

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = username = password   = None
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        print("validated succcessfully")
        email = signup_form.email.data
        username = signup_form.username.data
        password = signup_form.password.data
        existing_user = user.query.filter((email == user.email) | (username == user.username)).first()
        if existing_user :
            print("---------------")
            print(existing_user.email)
            print(existing_user.username)
            print(existing_user)
            print("---------------")
            print(signup_form.email.data)
            print(signup_form.username.data)
            print(signup_form.password.data)

            flash("Username or email is already in use, log in!")
            return redirect(url_for('auth.login'))
        db_entry = user(email=email, username=username, password=generate_password_hash(password, method='sha256'))
        try:
            db.session.add(db_entry)
            db.session.commit()
        except:
            return "Database error"
    return render_template('welcome.html', username=username)

@auth.route('/profile')
@login_required
def profile():
    return  render_template('profile.html',current_user=current_user)