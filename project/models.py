from . import db
from . import bcrypt

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

class BlogPost(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))
    category_id = db.Column(db.Integer, ForeignKey('categories.id'))
    comments = relationship("Comment", backref="post") # post.comments
    def __init__(self, title, description, author_id, category_id):
        self.title = title
        self.description = description
        self.author_id = author_id
        self.category_id = category_id

    def __repr__(self):
        return '<title {} | {} >'.format(self.title, self.description)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, ForeignKey('posts.id'))
    author_id = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, content, post_id, author_id):
        self.content = content
        self.post_id = post_id
        self.author_id = author_id

    def __repr__(self):
        return '<Comment {} >'.format(self.content)




class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    posts = relationship("BlogPost", backref="category")


    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<name {} >'.format(self.name)




class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    posts = relationship("BlogPost", backref="author")
    comments = relationship("Comment", backref="author") # comment.author.(id, name, email...)


    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<name {} >'.format(self.name)






