from . import users_blueprint
from flask import flash, redirect, url_for, render_template, abort, request
from project.models import User, BlogPost
from forms import LoginForm, RegisterForm
from project import bcrypt, LoginManager, db
from flask_login import login_user, logout_user, login_required




@users_blueprint.route('/<string:author>')
@users_blueprint.route('/u/<string:author>')
@users_blueprint.route('/user/<string:author>')
@login_required
def posts_by_author(author):
    author = User.query.filter_by(name = author).first()
    message = ""
    if author:
        posts = BlogPost.query.filter_by(author_id = author.id)
        if not posts.first():
            message = "No Articles Yet."
    else:
        abort(404)
    return render_template("posts_by_author.html", posts=posts, author = author, message = message)

@users_blueprint.route('/user/<string:username>/favorites')
@login_required
def fav_posts(username):
    user = User.query.filter_by(name = username).first()
    message = ""
    if user:
        posts = user.fav_posts
        if not posts.first():
            message = "No Favorites Yet."
    else:
        abort(404)
    return render_template("fav_posts.html", posts = posts, user = user, message = message)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    flash('You were logged in')
                    return redirect(url_for('posts.home'))
            else:
                    error = "Invalid!"
        else:
            return render_template('login.html', form = form, error=error)
    return render_template('login.html', form=form, error=error)

@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('posts.home'))


@users_blueprint.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
                name = form.username.data,
                email = form.email.data,
                password = form.password.data
                )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("You were logged in")
        return redirect(url_for('posts.home'))
    return render_template("register.html", form = form) 







