from flask import flash, redirect, session, url_for, render_template, abort, request

from project.models import BlogPost, User, Category

from  flask_login import current_user, login_required

from . import posts_blueprint
from forms import PostForm
from project import db

@posts_blueprint.route("/posts/<id>")
def post_by_id(id):
    post = BlogPost.query.filter_by(id = id).first_or_404()
    return render_template("post.html", post = post)

@posts_blueprint.route('/')
@login_required
def home():
    posts = BlogPost.query.all()
    user = current_user # Test if user is in the page
    return render_template("index.html", posts=posts, user=user)


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

@posts_blueprint.route('/add_post', methods=["GET", "POST"])
def add_post():
    form = PostForm()
    if request.method == "POST":
        if form.validate_on_submit():
            title = form.title.data
            description = form.description.data
            category = Category.query.filter_by(name = form.category.data).first()
            user_id = current_user.id
            if category:
                category_id = category.id
                post = BlogPost(title, description, user_id, category_id)
            else:
                db.session.add(Category(form.category.data))
                db.session.commit()
                flash("Added New category")
                category_id = Category.query.filter_by(name = form.category.data).first().id
                post = BlogPost(title, description, user_id, category_id)
            db.session.add(post)
            db.session.commit()
            flash("Added New Post")
            return redirect(url_for("posts.home"))
    return render_template("add_post.html", form=form)



