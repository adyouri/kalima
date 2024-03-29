import bcrypt

from flask import (flash, redirect, url_for,
                   render_template, abort,
                   request, g, jsonify, current_app)
from flask_login import login_user, logout_user, login_required, current_user

from . import users_blueprint
from project.models import User, BlogPost
from project.users.forms import LoginForm, RegisterForm, SettingsForm
from project import  LoginManager, db

def change_user_settings(email, current_password, new_password, private_favorites):
    message = None
    if current_user.email != email:
        current_user.email = email
    if (current_password != "" and\
            bcrypt.checkpw(
            current_password.encode('utf-8'), current_user.password)):
        current_user.update_password(new_password)
    elif (current_password == ""):
        message = None
    else:
        message = "Current password is incorrect"
    current_user.private_favorites = private_favorites
    if db.session.dirty:
        db.session.commit()
        flash('You have successfully changed your settings')
    return message

def check_and_add_user(name, email, password):
    check_username = User.query.filter_by(name = name).first()
    check_email = User.query.filter_by(email = email).first()
    if check_username and check_email:
        g.message =  "Email and Username already registered"
    elif check_username:
        g.message =  "Username Already Taken"
    elif check_email:
        g.message = "Email Already Registered"
    else:
        user = User(name, email, password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("You were logged in")
        return True

@users_blueprint.route('/<string:author>')
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

@users_blueprint.route('/<string:username>/favorites')
def fav_posts(username):
    user = User.query.filter_by(name = username).first()
    message = ""
    if user:
        if user.private_favorites and user != current_user:
            message = "You cannot access this page because this user's favorite posts are private!"
            posts = None
        else:
            posts = user.fav_posts
            if not posts.first():
                message = "No Favorites Yet."
    else:
        abort(404)
    return render_template("fav_posts.html", posts = posts, user = user, message = message)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_active:
        return redirect(url_for("posts.home"))
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=form.username.data).first()
            if user and bcrypt.checkpw(form.password.data.encode('utf-8'),
                                       user.password):
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
    if current_user.is_active:
        return redirect(url_for("posts.home"))
    form = RegisterForm()

    # form.username.errors
    # form.username(placeholder= 'Enter your username', required = True, value = 'Default Value')
    # form.username.errors

    # form.username.label
    # form.password.label

    g.message = ""
    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data
        password = form.password.data
        if check_and_add_user(name, email, password) == True:
            return redirect(url_for('posts.home'))
    return render_template("register.html", form = form)


@users_blueprint.route('/settings', methods=['POST', 'GET'])
@login_required
def settings():
    message = None
    form = SettingsForm()
    form.private_favs.default = current_user.private_favorites
    if form.validate_on_submit():
        email = form.email.data
        current_password = form.current_password.data
        new_password = form.new_password.data
        private_favs = form.private_favs.data
        message = change_user_settings(email=email,
                             current_password=current_password,
                             new_password=new_password,
                             private_favorites=private_favs)
        if not message:
            return redirect(url_for('users.settings'))
    return render_template('settings.html', form=form, message=message)

@users_blueprint.route('/<string:username>/follow')
@login_required
def follow(username):
    user = User.query.filter_by(name = username).first()
    current_user.follow(user)
    db.session.commit()
    return jsonify({"status": 200})


@users_blueprint.route('/<string:username>/unfollow')
@login_required
def unfollow(username):
    user = User.query.filter_by(name = username).first()
    current_user.unfollow(user)
    db.session.commit()
    return jsonify({"status": 200})

@users_blueprint.route('/<string:username>/profile')
def profile(username):
    message = None
    user = User.query.filter_by(name = username).first()
    posts = BlogPost.query.filter(BlogPost.author_id == user.id).order_by(BlogPost.created_date.desc()).limit(5)
    if not posts.first():
        message = "No Posts Yet"
    return render_template("profile.html",
                           posts = posts,
                           user = user,
                           message = message)

@users_blueprint.route('/<string:username>/followers')
def followers(username):
    user = User.query.filter_by(name = username).first()
    followers = {"followers": [user.name for user in user.followers.all()]}

    return jsonify(**followers)

@users_blueprint.route('/<string:username>/following')
def following(username):
    user = User.query.filter_by(name = username).first()
    following = {"following": [user.name for user in user.following.all()]}
    return jsonify(**following)
