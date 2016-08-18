from datetime import datetime
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object(os.environ['APP_SETTINGS'])

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
from posts import posts_blueprint
from users import users_blueprint

app.register_blueprint(posts_blueprint)
app.register_blueprint(users_blueprint)

from models import User, Category

login_manager.login_view = "users.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id = int(user_id)).first()

@app.template_filter()
def slugify(string):
    return string.lower().replace(" ", "-")

@app.context_processor
def categories():
    categories = Category.query.all()
    return dict(categories=categories)

@app.template_filter()
def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

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
