import unittest
from flask_testing import TestCase
from flask_login import current_user
from project import app, db
from project.models import BlogPost, User, Category

class BaseTestCase(TestCase):
    """The Base Test Case"""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User("admin", "admin@g.co", "admin"))
        db.session.add(User("abd", "abd@g.co", "abd"))
        db.session.add(Category("testing"))
        db.session.add(BlogPost("Testing Post", "This is just a test post", 1, 1))
        db.session.add(BlogPost("From Abd", "This is just a test post From Abd", 2, 1))
        db.session.commit()



    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):
        def test_index(self):
            response = self.client.get('/login', content_type='html/text')
            self.assertEqual(response.status_code, 200)

        def test_welcome(self):
            response = self.client.get('/welcome', content_type='html/text')
            self.assertIn("welcome", response.data)

        def test_post_show_up(self):
            self.client.post(
                                    '/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = self.client.get('/', follow_redirects=True)
            self.assertIn(b'This is just a test post From Abd', response.data)

        def test_post_in_category(self):
            self.client.post(
                                    '/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = self.client.get('/cat/testing', follow_redirects=True)
            self.assertIn(b'This is just a test post', response.data)

        def test_page_not_found(self):
            self.client.post(
                                    '/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)

            response = self.client.get('/not_existing_page_or_user', follow_redirects=False)
            self.assertEqual(response.status_code, 404)

        def test_category_not_found(self):
            self.client.post(
                                    '/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)

            response = self.client.get('/cat/not_existing_category', follow_redirects=False)
            self.assertEqual(response.status_code, 404)


class UsersTestCase(BaseTestCase):

        def test_user_not_found(self):
            self.client.post(
                                    '/login',
                                    data=dict(
                                        username="admin",
                                        password="admin"),
                                        follow_redirects = True)

            response = self.client.get('/u/not_existing_user', follow_redirects=False)
            response1 = self.client.get('/user/not_existing_user', follow_redirects=False)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response1.status_code, 404)

        def test_post_by_author(self):
            self.client.post(
                                    '/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = self.client.get('/u/abd', follow_redirects=True)
            response1 = self.client.get('/admin', follow_redirects=True)
            response2 = self.client.get('/user/admin', follow_redirects=True)
            self.assertIn(b'From Abd', response.data)
            self.assertIn(b'test post', response1.data)
            self.assertIn(b'just a test', response2.data)

        def test_correct_login(self):
            with self.client:
                response = self.client.post(
                                        '/login',
                                        data=dict(username="admin", password="admin"),
                                        follow_redirects = True)
                self.assertIn(b'You were logged in', response.data)
                self.assertTrue(current_user.name == "admin")
                self.assertTrue(current_user.is_active())



        def test_incorrect_login(self):
            response = self.client.post(
                                    '/login',
                                    data=dict(username="wrong", password="admin"),
                                    follow_redirects = True)
            self.assertIn(b'Invalid', response.data)
        def test_logout(self):
            with self.client:
                self.client.post(
                                        '/login',
                                        data=dict(username="admin", password="admin"),
                                        follow_redirects = True)
                response = self.client.get('/logout', follow_redirects=True)
                self.assertIn(b'Please login', response.data)
                self.assertFalse(current_user.is_active())

        def test_login_page_loads(self):
            response = self.client.get('/login', content_type='html/text')
            self.assertTrue(b'Please login' in response.data)

        def test_main_route_requires_login(self):
            response = self.client.get('/', follow_redirects=True)
            self.assertIn(b'Please login', response.data)

        def test_correct_registration(self):
            with self.client:
                response = self.client.post(
                                        '/register',
                                        data=dict(username="test_user",
                                            email="test@email.co",
                                            password="testpassword",
                                            confirm="testpassword"),
                                        follow_redirects = True)
                self.assertIn(b'You were logged in', response.data)
                self.assertTrue(current_user.name == "test_user")
                self.assertTrue(current_user.is_active())

        def test_incorrect_registration(self):
            with self.client:
                response = self.client.post(
                                        '/register',
                                        data=dict(username="",
                                            email="teco",
                                            password="test",
                                            confirm="testpassword"),
                                        follow_redirects = True)
                self.assertIn(b'Must Provide An Actual Email :)', response.data)
                self.assertIn(b'Field must be between 6 and 25 characters long.', response.data)
                self.assertIn(b'Passwords must match', response.data)
                self.assertIn(b'This field is required.', response.data)






if __name__ == '__main__':
    unittest.main()
