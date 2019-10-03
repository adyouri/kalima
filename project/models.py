from . import db
from . import bcrypt

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


# many-to-many relationship table | post.tags / tag.posts
posts_tags = db.Table(
        "posts_tags",
        db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), nullable=False),
        db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), nullable=False),
        db.PrimaryKeyConstraint('post_id', 'tag_id')
        )

# many-to-many relationship table | user.fav_posts / post.fav_users
favs = db.Table(
        "favs",
        db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), nullable=False),
        db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
        db.PrimaryKeyConstraint('post_id', 'user_id')
        )



# many-to-many relationship table | user.fav_posts / post.fav_users
follows = db.Table(
        "follows",
        db.Column('follower_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
        db.Column('followed_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
        )


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self, name):
        self.name = name


class BlogPost(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))
    category_id = db.Column(db.Integer, ForeignKey('categories.id'))
    comments = relationship("Comment", backref="post") # post.comments
    created_date = db.Column(db.DateTime)
    tags = db.relationship('Tag', secondary = posts_tags, backref = db.backref("posts", lazy = "dynamic"))
    fav_users = db.relationship('User', secondary = favs, backref = db.backref("fav_posts", lazy = "dynamic"))
    """
    def __init__(self, title, description, author_id, category_id, created_date = None):
        self.title = title
        self.description = description
        self.author_id = author_id
        self.category_id = category_id
        self.created_date = datetime.utcnow()
     """
    def __init__(self, title, description, author_id, created_date = None):
        self.title = title
        self.description = description
        self.author_id = author_id
        self.created_date = datetime.utcnow()

    def __repr__(self):
        return '<title {} | {} >'.format(self.title, self.description)



class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, ForeignKey('posts.id'))
    author_id = db.Column(db.Integer, ForeignKey('users.id'))
    created_date = db.Column(db.DateTime)

    def __init__(self, content, post_id, author_id, created_date = None):
        self.content = content
        self.post_id = post_id
        self.author_id = author_id
        self.created_date = datetime.utcnow()

    def __repr__(self):
        return '<Comment {} >'.format(self.content)




class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    posts = relationship("BlogPost", backref="category")


    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<name {} >'.format(self.name)




class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    private_favorites = db.Column(db.Boolean, default = True)
    posts = relationship("BlogPost", backref="author")
    comments = relationship("Comment", backref="author") # comment.author.(id, name, email...)


    # questions_to = 
    # questions_from = 



    following = relationship("User",
                             secondary=follows,
                             primaryjoin=(follows.c.follower_id == id),
                             secondaryjoin=(follows.c.followed_id == id),
                             backref=db.backref("followers",
                                                 lazy= "dynamic"),
                             lazy = "dynamic")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password.encode('utf-8'))

    def update_password(self, password):
        """ Because Bcrypt doesn't hash the password when updating (user.password = "new") """
        self.password = bcrypt.generate_password_hash(password.encode('utf-8'))

    def is_following(self, user):
        return self.following.filter(follows.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)
            return self
    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)
            return self


    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<name {} >'.format(self.name)

# User to User questions, Each user can submit a question to another user
# A user can only access and answer questions directed to them
# User can question other users

asker_asked = db.Table(
        "asker_asked",
        db.Column('question_id', db.Integer, db.ForeignKey('questions.id'), nullable=False),
        db.Column('asker_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
        db.Column('asked_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
        )
# 1 | 2 | 1 ===> user1 asks user2 the question1
# question1.asker >> user1
# question2.asked >> user2
# question.answer (easy)

class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    #asker = db.relationship
    """
    following = relationship("User",
                             secondary=follows,
                             primaryjoin=(follows.c.follower_id == id),
                             secondaryjoin=(follows.c.followed_id == id),
                             backref=db.backref("followers",
                                                 lazy= "dynamic"),
                             lazy = "dynamic")
    """
    asked = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    answer = db.Column(db.String(200))

    def __init__(self, content):
        self.content = content

