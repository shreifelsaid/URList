from flask import Flask, render_template, redirect
from flask.helpers import url_for
from forms import *
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_login import LoginManager, current_user, login_required
from werkzeug.utils import secure_filename
import os
import uuid



IMAGE_UPLOAD_FOLDER = '/static/img'
EXTENSIONS = set(['jpg', 'jpeg'])

app = Flask(__name__)
application = app
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
from models import *
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

bootstrap = Bootstrap(app)
moment = Moment(app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    old_post = posts.query.get(id)
    update_form = UpdateForm(title=old_post.title, body=old_post.body,price=old_post.price,pic=old_post.pic)
        
    if update_form.validate_on_submit():

        old = posts.query.get_or_404(id)
        old.title = update_form.title.data
        old.body = update_form.body.data
        old.price = update_form.price.data
        pic = update_form.pic.data
        uuid_filename = str(uuid.uuid4())
        pic.save(os.path.join(
            app.root_path, 'static/img', uuid_filename
        ))
        old.pic = uuid_filename
        print(update_form.title.data)
        print(update_form.body.data)
        print(update_form.price.data)
        print(uuid_filename)

        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "Update error"
    return render_template('update.html', update_form=update_form )

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    deleted_post = posts.query.get_or_404(id)
    try:
        db.session.delete(deleted_post)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "Delete error"

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    title = body = price = pic = None
    post_form = PostForm()
    if post_form.validate_on_submit():
        title = post_form.title.data
        body = post_form.body.data
        price = post_form.price.data
        pic = post_form.pic.data
        uuid_filename = str(uuid.uuid4())
        pic.save(os.path.join(
            app.root_path, 'static/img', uuid_filename
        ))
        
        db_entry = posts(title = title, body = body, price = price, pic = uuid_filename, author_username=current_user.username, author_email=current_user.email)
        try:
            db.session.add(db_entry)
            db.session.commit()
        except:
            return "Database error"
    else :
        print(post_form.errors)

    return render_template('index.html', post_form=post_form , posts_table=posts.query.order_by(posts.id.desc()).all(), current_user=current_user)


