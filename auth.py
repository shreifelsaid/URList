from flask.helpers import flash
from werkzeug import security
from flask_login import  login_user, logout_user, login_required, current_user
from models import user, db
from forms import LoginForm, ResetPasswordForm, ResetUsernameForm, SignupForm
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
    email = username = password = security_question = security_answer  = None
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        print("validated succcessfully")
        email = signup_form.email.data
        username = signup_form.username.data
        password = signup_form.password.data
        security_question = signup_form.security_question.data
        security_answer = signup_form.security_answer.data
        existing_user = user.query.filter((email == user.email) | (username == user.username)).first()
        if existing_user :
            print("---------------")
            print(existing_user.email)
            print(existing_user.username)
            print(existing_user.security_question)
            print(existing_user.security_answer)
            print("---------------")
            print(signup_form.email.data)
            print(signup_form.username.data)
            print(signup_form.password.data)
            print(signup_form.security_question.data)
            print(signup_form.security_answer.data)

            flash("Username or email is already in use, log in!")
            return redirect(url_for('auth.login'))
        db_entry = user(email=email, username=username, password=generate_password_hash(password, method='sha256'),security_question=security_question, security_answer=generate_password_hash(security_answer, method='sha256'))
        try:
            db.session.add(db_entry)
            db.session.commit()
        except:
            return "Database error"
    return render_template('welcome.html', username=username)

@auth.route('/profile',methods=['GET','POST'])
@login_required
def profile():

    password_reset_form = ResetPasswordForm()
    username_reset_form = ResetUsernameForm()

    existing_user = user.query.filter_by(email = current_user.email).first()
    security_question_dict = {
    1 : 'What was your childhood nickname?',
    2 : 'What is the name of your favorite childhood friend?',
    3 : 'What was the last name of your third grade teacher?',
    4 : 'In what city or town was your first job?',
    5 : 'What was the name of your first stuffed animal?',
    6 : 'What is the name of a college you applied to but didn\'t attend?',
    }
    security_question = security_question_dict[existing_user.security_question]
    existing_answer = existing_user.security_answer
    existing_password = existing_user.password
    if password_reset_form.validate_on_submit():
        security_answer = password_reset_form.security_answer.data
        old_password = password_reset_form.old_password.data
        new_password = password_reset_form.new_password

        if not check_password_hash(existing_password, old_password) or not check_password_hash(existing_answer, security_answer):
            flash("wrong password or security answer")
            return redirect(url_for('auth.profile'))

        existing_user.password = generate_password_hash(new_password, method='sha256')
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "Update error"

    if username_reset_form.validate_on_submit():

        security_answer = username_reset_form.security_answer.data
        old_password = username_reset_form.old_password.data
        new_username = username_reset_form.new_username

        if not check_password_hash(existing_password, old_password) or not check_password_hash(existing_answer, security_answer):
            flash("wrong password or security answer")
            return redirect(url_for('auth.profile'))
        user_already_exists = user.query.filter_by(username = new_username).first()
        if user_already_exists:
            flash("username is taken")
            return redirect(url_for('auth.profile'))

        existing_user.username = new_username
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "Update error"

    return  render_template('profile.html',current_user=current_user, password_reset_form=password_reset_form,username_reset_form=username_reset_form,security_question=security_question)