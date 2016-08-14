import unittest
from flask_testing import TestCase
from flask_login import current_user
from project import app, db
from project.models import BlogPost, User, Category, Comment

class BaseTestCase(TestCase):
    """The Base Test Case"""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User("admin", "admin@g.co", "admin"))
        db.session.add(User("abd", "abd@g.co", "abd"))
        db.session.add(User("tester", "tester@g.co", "tester"))
        db.session.add(Category("testing"))
        db.session.add(BlogPost("Testing Post", "This is just a test post", 1, 1))
        db.session.add(BlogPost("From Abd", "This is just a test post From Abd", 2, 1))
        db.session.add(Comment("Test comment", 1, 2))
        db.session.commit()



    def tearDown(self):
        db.session.remove()
        db.drop_all()


