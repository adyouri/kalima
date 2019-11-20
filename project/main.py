import os
import re
from datetime import datetime

from flask import Flask, render_template, abort, Blueprint, current_app
from sqlalchemy.sql.expression import func

from project.models import User, Category, Comment, BlogPost

from project import create_app


main_blueprint = Blueprint("main",
                    __name__,
                    template_folder='templates')


@main_blueprint.route('/')
def index():
    posts = BlogPost.query.limit(5)
    return render_template('index.html', posts = posts)


# Error for testing
@main_blueprint.route('/500')
def error_500():
    abort(500)



