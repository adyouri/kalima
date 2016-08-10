from . import users_blueprint
from project.decorators import login_required
from flask import flash, redirect, session, url_for, render_template, abort, request
from project.models import User, BlogPost

@users_blueprint.route('/<author>')
@users_blueprint.route('/u/<author>')
@users_blueprint.route('/user/<author>')
@login_required
def posts_by_author(author):
    author = User.query.filter_by(name = author).first()
    if author:
        posts = BlogPost.query.filter_by(author_id = author.id)
    else:
        abort(404)
    return render_template("posts_by_author.html", posts=posts, author = author)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != "admin" or request.form['password'] != "admin":
            error = "Invalid!"
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('posts.home'))
    return render_template('login.html', error=error)

@users_blueprint.route('/logout')
@login_required
def logout():
    session.pop('logged_in')
    flash('Logged out successfully !')
    return redirect(url_for('posts.home'))
#def connect_db():
#    return sqlite3.connect(app.database)




