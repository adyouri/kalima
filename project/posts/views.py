# -*- coding: utf-8 -*-
from flask import (flash, redirect, session,
                   url_for, render_template,
                   abort, request, jsonify)

from project.models import BlogPost, User, Category, Comment, Tag

from  flask_login import current_user, login_required

from . import posts_blueprint
from forms import PostForm, CommentForm
from project import db



@posts_blueprint.route("/<int:id>", methods=["GET", "POST"])
def post_by_id(id):
    post = BlogPost.query.filter_by(id = id).first_or_404()
    comments = Comment.query.filter_by(post_id = post.id)
    form = CommentForm()
    if form.validate_on_submit():
        db.session.add(Comment(form.content.data, post.id, current_user.id))
        db.session.commit()
        flash("Added new comment successfully!")
    return render_template("post.html", post = post, comments = comments, form = form)


@posts_blueprint.route('/<int:id>/fav')
@login_required
def add_fav(id):
    post = BlogPost.query.filter_by(id = id).first_or_404()
    if current_user not in post.fav_users:
        post.fav_users.append(current_user)
        db.session.commit()
        flash('post "{}" was successfully added to your favorites'.format(post.id))
    else:
        flash("Already added to your favorites")
    return redirect(url_for("posts.post_by_id",
                            id = id))


@posts_blueprint.route('/<int:id>/fav_users')
def fav_users_list(id):
    post = BlogPost.query.filter_by(id = id).first_or_404()
    fav_users_list = [user.name for user in post.fav_users]
    
    return jsonify(**{"fav_users_list": fav_users_list})







@posts_blueprint.route('/<int:id>/unfav')
@login_required
def remove_fav(id):
    post = BlogPost.query.filter_by(id = id).first_or_404()
    post.fav_users.remove(current_user)
    db.session.commit()
    flash('post "{}" was successfully removed from your favorites'.format(post.id))
    return redirect(url_for("posts.post_by_id",
                            id = id))


@posts_blueprint.route('/')
def home():
    posts = BlogPost.query.all()
    return render_template("posts.html", posts=posts)


@posts_blueprint.route('/cat/<category>')
def posts_by_category(category):
    category = Category.query.filter_by(name = category).first_or_404()
    message = ""
    if category:
        posts = BlogPost.query.filter_by(category_id = category.id)
        if not posts.first():
            message = "No Articles Yet."
    return render_template("posts_by_category.html",
                            posts = posts,
                            category = category,
                            message = message)
@posts_blueprint.route('/tag/<tag>')
def posts_by_tag(tag):
    tag = Tag.query.filter_by(name = tag).first_or_404()
    posts = tag.posts
    return render_template("posts_by_tag.html",
                            posts = posts,
                            tag = tag,
                            )

@posts_blueprint.route('/welcome')
def welcome():
    return render_template("welcome.html")

@posts_blueprint.route('/new', methods=["GET", "POST"])
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
            tags = form.tags.data.split(" ")
            # check if tag exists and if it is already added to the post (Ugly, refactor it): 
            for tag in tags:
                t = Tag(tag)
                tag_exists = Tag.query.filter_by(name = tag).first()
                if tag_exists:
                        if tag_exists not in post.tags:
                            post.tags.append(tag_exists)
                        else:
                            pass
                else:
                    db.session.add(t)
                    post.tags.append(t)
                    db.session.commit()
                    
            db.session.add(post)
            db.session.commit()
            flash("Added New Post")
            return redirect(url_for("posts.home"))
    return render_template("add_post.html", form=form)



