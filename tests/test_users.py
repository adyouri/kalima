import unittest
from flask_login import current_user
from base import BaseTestCase
from project import bcrypt
from project.models import User


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
            response3 = self.client.get('/user/tester', follow_redirects=True)
            self.assertIn(b'From Abd', response.data)
            self.assertIn(b'Testing Post', response2.data)
            self.assertIn(b'No Articles Yet.', response3.data)

        def test_correct_login(self):
            with self.client:
                response = self.client.post(
                                        '/login',
                                        data=dict(username="admin", password="admin"),
                                        follow_redirects = True)
                self.assertIn(b'You were logged in', response.data)
                self.assertTrue(current_user.name == "admin")
                user = User.query.filter_by(name="admin").first()
                self.assertTrue(str(user) == "<name admin >")
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
        def test_check_password(self):
            user = User.query.filter_by(name="admin").first()
            self.assertTrue(bcrypt.check_password_hash(user.password, "admin"))
            self.assertFalse(bcrypt.check_password_hash(user.password, "incorrect"))







if __name__ == '__main__':
    unittest.main()
