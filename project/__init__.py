from flask import Flask
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
import os
app.config.from_object(os.environ['APP_SETTINGS'])

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
from posts import posts_blueprint
from users import users_blueprint

app.register_blueprint(posts_blueprint)
app.register_blueprint(users_blueprint)




