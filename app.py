from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
application = app
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

class posts(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(500), nullable = False)
    body = db.Column(db.String(500), nullable = False)
    price = db.Column(db.String(500), nullable = False)
    pic = db.Column(db.String(500), nullable = False)

    def __repr__(self):
        return self


class PostForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    body = StringField('Description:', validators=[DataRequired()])
    price = StringField('Price:', validators=[DataRequired()])
    pic = StringField('Photo:', validators=[DataRequired()])

    submit = SubmitField('Post!')

class UpdateForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    body = StringField('Description:', validators=[DataRequired()])
    price = StringField('Price:', validators=[DataRequired()])
    pic = StringField('Photo:', validators=[DataRequired()])

    submit = SubmitField('Update!')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    old_post = posts.query.get(id)
    update_form = UpdateForm()
    # update_form.user_ingredient.data = old_ingredient
    if update_form.validate_on_submit():
        old = posts.query.get_or_404(id)
        old.title = update_form.title.data
        old.body = update_form.body.data
        old.price = update_form.price.data
        old.pic = update_form.pic.data
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Update error"
    return render_template('update.html', update_form=update_form)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    deleted_post = posts.query.get_or_404(id)
    try:
        db.session.delete(deleted_post)
        db.session.commit()
        return redirect('/')
    except:
        return "Delete error"

@app.route('/', methods=['GET', 'POST'])
def index():
    title = body = price = pic = None
    post_form = PostForm()
    if post_form.validate_on_submit():
        title = post_form.title.data
        body = post_form.body.data
        price = post_form.price.data
        pic = post_form.pic.data

        db_entry = posts(title = title, body = body, price = price, pic = pic )
        try:
            db.session.add(db_entry)
            db.session.commit()
        except:
            return "Database error"

    return render_template('index.html', post_form=post_form , posts_table=posts.query.all())
