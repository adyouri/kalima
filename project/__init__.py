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

from models import User

login_manager.login_view = "users.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id = int(user_id)).first()

