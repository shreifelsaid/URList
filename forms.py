from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired

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
    email = StringField('email:', validators=[DataRequired()])
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Signup!')

class LoginForm(FlaskForm):
    email = StringField('email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login!')

class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Password:', validators=[DataRequired()])
    new_password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login!')
