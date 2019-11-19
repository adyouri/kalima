import unittest
from flask_testing import TestCase
from flask_login import current_user
from project import create_app, db
from project.models import BlogPost, User, Category, Comment, Tag

class BaseTestCase(TestCase):
    """The Base Test Case"""

    def create_app(self):
        app = create_app(testing=True)
        return app

    def setUp(self):
        #self.create_app() # Create the app with TestConfig
        db.create_all()
        admin = User("admin", "admin@g.co", "admin")
        admin.private_favorites = True
        db.session.add(admin)
        db.session.add(User("abd", "abd@g.co", "abd"))
        db.session.add(User("tester", "tester@g.co", "tester"))
        c = Category("testing")
        db.session.add(c)
        db.session.add(Category("testing_cat"))
        testing_post = BlogPost("Testing Post", "This is just a test post", author_id=1)
        testing_post.category = c
        db.session.add(testing_post)
        post1 = BlogPost("Testing Tag", "This is just a test post to test tags", author_id=2)
        post2 = BlogPost("From Abd", "This is just a test post From Abd", author_id=2)
        post1.category = c
        post2.category = c
        db.session.add(post1)
        db.session.add(post2)
        tag = Tag("tests")
        post1.tags.append(tag)
        db.session.add(Comment("Test comment", 1, 2))
        admin.fav_posts.append(testing_post)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


