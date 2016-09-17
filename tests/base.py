import unittest
from flask_testing import TestCase
from flask_login import current_user
from project import app, db
from project.models import BlogPost, User, Category, Comment, Tag

class BaseTestCase(TestCase):
    """The Base Test Case"""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        admin = User("admin", "admin@g.co", "admin")
        admin.private_favorites = True
        db.session.add(admin)
        db.session.add(User("abd", "abd@g.co", "abd"))
        db.session.add(User("tester", "tester@g.co", "tester"))
        db.session.add(Category("testing"))
        testing_post = BlogPost("Testing Post", "This is just a test post", 1, 1)
        db.session.add(testing_post)
        db.session.add(BlogPost("From Abd", "This is just a test post From Abd", 2, 1))
        post = BlogPost("Testing Tag", "This is just a test post to test tags", 2, 1)
        db.session.add(post)
        tag = Tag("tests")
        post.tags.append(tag)
        db.session.add(Comment("Test comment", 1, 2))
        admin.fav_posts.append(testing_post)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


