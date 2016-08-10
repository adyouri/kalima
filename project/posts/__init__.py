from flask import Blueprint

posts_blueprint = Blueprint("posts", __name__, template_folder='templates')

import views
