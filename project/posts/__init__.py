from flask import Blueprint

posts_blueprint = Blueprint("posts", __name__, template_folder='templates', url_prefix='/posts')

from . import views
