# -*- coding: utf-8 -*-


import os

from flask import Flask, render_template, abort
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


login_manager = LoginManager()
db = SQLAlchemy()

from project.models import User, Category, Comment, BlogPost
from project.cli import run_tests_command, coverage_command


def create_app(testing=False):
    app = Flask(__name__)
    if testing:
        app.config.from_object('config.TestConfig')
    else:
        app.config.from_object(os.environ['APP_SETTINGS'])

    login_manager.init_app(app)
    db.init_app(app)

    from project.main import main_blueprint
    from project.posts import posts_blueprint
    from project.users import users_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(posts_blueprint)
    app.register_blueprint(users_blueprint)

    from project.filters import timesince, slugify
    app.jinja_env.filters['timesince'] = timesince
    app.jinja_env.filters['slugify'] = slugify

    from project.utils import latest_comments, post_by_id, random_posts


    @app.context_processor
    def inject_data():
        categories = Category.query.all()
        return dict(categories = [category.name for category in categories if category != None],
                    latest_comments = latest_comments(),
                    post_by_id = post_by_id,
                    random_posts = random_posts(),
                    )

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html')

    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('500.html')

    app.cli.add_command(run_tests_command)
    app.cli.add_command(coverage_command)

    return app

login_manager.login_view = "users.login"
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id = int(user_id)).first()
