from flask import flash, redirect, session, url_for, render_template, abort

from project.models import BlogPost, User, Category





from . import posts_blueprint
from project.decorators import login_required
@posts_blueprint.route("/posts/<id>")
def post_by_id(id):
    post = BlogPost.query.filter_by(id = id).first_or_404()
    return render_template("post.html", post = post)

@posts_blueprint.route('/')
@login_required
def home():
    posts = BlogPost.query.all()
    return render_template("index.html", posts=posts)


@posts_blueprint.route('/cat/<category>')
@login_required
def posts_by_category(category):
    category = Category.query.filter_by(name = category).first()
    if category:
        posts = BlogPost.query.filter_by(category_id = category.id)
    else:
        abort(404)
    return render_template("posts_by_category.html", posts = posts, category = category)



@posts_blueprint.route('/welcome')
def welcome():
    return render_template("welcome.html")


