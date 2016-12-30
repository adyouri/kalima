# -*- coding: utf-8 -*-


from datetime import datetime
from flask import Flask, render_template, abort
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import re

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object(os.environ['APP_SETTINGS'])

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
db = SQLAlchemy(app)
from posts import posts_blueprint
from users import users_blueprint

app.register_blueprint(posts_blueprint)
app.register_blueprint(users_blueprint)

from models import User, Category, Comment, BlogPost

login_manager.login_view = "users.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id = int(user_id)).first()

@app.template_filter()
def slugify(string):
    """ Does not work with arabic """
    return re.sub('[^\w]+', '-', string.lower())

def latest_comments():
    comments_list = []
    comments = Comment.query.order_by(Comment.created_date.desc()) # latest added comments
    for comment in comments:
        if comment.created_date:
            comments_list.append(comment)
        else:
            pass
    return comments_list[:5] # only the first five recently added comments

def post_by_id(post_id):
    post = BlogPost.query.filter_by(id = post_id).first()
    return post


random_posts = BlogPost.query.order_by(func.random()).limit(3)

@app.context_processor
def categories():
    categories = Category.query.all()
    return dict(categories = [category.name for category in categories if category != None],
                latest_comments = latest_comments,
                post_by_id = post_by_id,
                random_posts = random_posts,
                )

################## Main Routes ################## 
@app.route('/')
def index():
    posts = BlogPost.query.limit(5)
    return render_template('index.html', posts = posts)

@app.route('/500')
def error_500():
    abort(500)
    #return


@app.template_filter()
def timesince(dt, default="just now"):
    now = datetime.utcnow()
    diff = now - dt
    
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html')

