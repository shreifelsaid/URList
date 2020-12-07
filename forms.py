from werkzeug import security
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField

#TODO : make sure string fields can only take as much chars as db can handle

class PostForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    body = TextAreaField('Description:', validators=[DataRequired()])
    price = StringField('Price:', validators=[DataRequired()])
    pic = FileField(validators=[FileRequired()]) 
    submit = SubmitField('Post')

class UpdateForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    body = TextAreaField('Description:', validators=[DataRequired()])
    price = StringField('Price:', validators=[DataRequired()])
    pic = FileField(validators=[FileRequired()]) 
    submit = SubmitField('Update!')

class SignupForm(FlaskForm):
    email = EmailField('email:', validators=[DataRequired()])
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    security_question = SelectField(u'Security question:', choices=[
    (1, 'What was your childhood nickname?'), 
    (2, 'What is the name of your favorite childhood friend?'), 
    (3, 'What was the last name of your third grade teacher?'), 
    (4, 'In what city or town was your first job?'), 
    (5, 'What was the name of your first stuffed animal?'), 
    (6, 'What is the name of a college you applied to but didn\'t attend?')])
    security_answer = StringField('Answer:', validators=[DataRequired()])
    submit = SubmitField('Signup!')

class LoginForm(FlaskForm):
    email = StringField('Username or Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login!')

class ForgotLoginForm(FlaskForm):
    email = StringField('Username or Email:', validators=[DataRequired()])
    security_question = SelectField(u'Security question:', choices=[
    (1, 'What was your childhood nickname?'), 
    (2, 'What is the name of your favorite childhood friend?'), 
    (3, 'What was the last name of your third grade teacher?'), 
    (4, 'In what city or town was your first job?'), 
    (5, 'What was the name of your first stuffed animal?'), 
    (6, 'What is the name of a college you applied to but didn\'t attend?')])
    security_answer = StringField('Answer:', validators=[DataRequired()])
    submit = SubmitField('Login!')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('Password:', validators=[DataRequired()])
    security_answer = StringField('Answer:', validators=[DataRequired()])
    submit = SubmitField('Login!')

class ResetUsernameForm(FlaskForm):
    old_password = PasswordField('Password:', validators=[DataRequired()])
    new_username = StringField('Password:', validators=[DataRequired()])
    security_answer = StringField('Answer:', validators=[DataRequired()])
    submit = SubmitField('Login!')