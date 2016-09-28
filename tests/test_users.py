import unittest
from flask_login import current_user
from base import BaseTestCase
from project import bcrypt, db
from project.models import User


class UsersTestCase(BaseTestCase):

        def test_user_not_found(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(
                                        username="admin",
                                        password="admin"),
                                        follow_redirects = True)

            response = self.client.get('/users/not_existing_user', follow_redirects=False)
            self.assertEqual(response.status_code, 404)

        def test_post_by_author(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = self.client.get('/users/abd', follow_redirects=True)
            response2 = self.client.get('/users/admin', follow_redirects=True)
            response3 = self.client.get('/users/tester', follow_redirects=True)
            self.assertIn(b'From Abd', response.data)
            self.assertIn(b'Testing Post', response2.data)
            self.assertIn(b'No Articles Yet.', response3.data)

        def test_correct_login(self):
            with self.client:
                response = self.client.post(
                                        '/users/login',
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
                                    '/users/login',
                                    data=dict(username="wrong", password="admin"),
                                    follow_redirects = True)
            self.assertIn(b'Invalid', response.data)
        def test_logout(self):
            with self.client:
                self.client.post(
                                        '/users/login',
                                        data=dict(username="admin", password="admin"),
                                        follow_redirects = True)
                response = self.client.get('/users/logout', follow_redirects=True)
                self.assertIn(b'Please login', response.data)
                self.assertFalse(current_user.is_active())

        def test_login_page_loads(self):
            response = self.client.get('/users/login', content_type='html/text')
            self.assertTrue(b'Please login' in response.data)

        def test_main_route_requires_login(self):
            response = self.client.get('/posts/', follow_redirects=True)
            self.assertIn(b'Please login', response.data)

        def test_correct_registration(self):
            with self.client:
                response = self.client.post(
                                        '/users/register',
                                        data=dict(username="test_user",
                                            email="test@email.co",
                                            password="testpassword",
                                            confirm="testpassword"),
                                        follow_redirects = True)
                self.assertIn(b'You were logged in', response.data)
                self.assertTrue(current_user.name == "test_user")
                self.assertTrue(current_user.is_active())

        def test_username_is_already_taken(self):
            with self.client:
                response = self.client.post(
                                        '/users/register',
                                        data=dict(username="abd",
                                            email="testing@email.co",
                                            password="testpassword",
                                            confirm="testpassword"),
                                        follow_redirects = True)
                self.assertIn(b'Username Already Taken', response.data)
                self.assertFalse(current_user.is_active())

        def test_email_is_already_registered(self):
            with self.client:
                response = self.client.post(
                                        '/users/register',
                                        data=dict(username="testing_user",
                                            email="admin@g.co",
                                            password="testpassword",
                                            confirm="testpassword"),
                                        follow_redirects = True)
                self.assertIn(b'Email Already Registered', response.data)
                self.assertFalse(current_user.is_active())

        def test_email_username_already_registered(self):
            with self.client:
                response = self.client.post(
                                        '/users/register',
                                        data=dict(username="abd",
                                            email="admin@g.co",
                                            password="testpassword",
                                            confirm="testpassword"),
                                        follow_redirects = True)
                self.assertIn(b'Email and Username already registered', response.data)
                self.assertFalse(current_user.is_active())

        def test_incorrect_registration(self):
            with self.client:
                response = self.client.post(
                                        '/users/register',
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

        def test_redirecting_on_login_if_user_is_active(self):
            with self.client:
                self.client.post(
                                        '/users/login',
                                        data=dict(username="admin", password="admin"),
                                        follow_redirects = True)

                response = self.client.get(
                                        '/users/login',
                                        follow_redirects = True)

                self.assertTrue(current_user.is_active())
                self.assertIn(b'Testing Post', response.data)


        def test_redirecting_on_register_if_user_is_active(self):
            with self.client:
                self.client.post(
                                        '/users/login',
                                        data=dict(username="admin", password="admin"),
                                        follow_redirects = True)

                response = self.client.get(
                                        '/users/register',
                                        follow_redirects = True)

                self.assertTrue(current_user.is_active())
                self.assertIn(b'Testing Post', response.data)

        def test_correct_settings(self):
            with self.client:
                self.client.post(
                                        '/users/login',
                                        data=dict(username="admin", password="admin"),
                                        follow_redirects = True)

            with self.client:
                response = self.client.post(
                                        '/users/settings',
                                        data=dict(
                                            email="admin@example.com",
                                            current_password="admin",
                                            new_password="admino",
                                            confirm="admino",
                                            private_favs=False),
                                            follow_redirects = True)
                self.assertIn(b'You have successfully changed your settings', response.data)
                self.assertTrue(bcrypt.check_password_hash(current_user.password, "admino" ))
                self.assertFalse(bcrypt.check_password_hash(current_user.password, "incorrect" ))
                self.assertTrue(current_user.is_active())
                self.assertTrue(current_user.email == "admin@example.com")

        def test_follow(self):
            admin = User.query.get(1)
            abd   = User.query.get(2)

            admin.follow(abd)
            db.session.commit()
            self.assertTrue(admin.is_following(abd))
            self.assertFalse(abd.is_following(admin))

        def test_unfollow(self):
            admin = User.query.get(1)
            abd   = User.query.get(2)

            abd.follow(admin)
            db.session.commit()
            self.assertTrue(abd.is_following(admin))
            abd.unfollow(admin)
            db.session.commit()
            self.assertFalse(abd.is_following(admin))

        def test_following_list(self):
            self.client.post(
                        '/users/login',
                        data = dict(username="admin",
                                    password="admin")
                        )
            self.client.get('/users/abd/follow')
            response = self.client.get('/users/admin/following')
            self.assertIn('abd', response.data)
                        
        def test_following_list_after_unfollow(self):
            self.client.post(
                        '/users/login',
                        data = dict(username="admin",
                                    password="admin")
                        )
            self.client.get('/users/abd/follow')
            response = self.client.get('/users/admin/following')
            self.assertIn('abd', response.data)
            self.client.get('/users/abd/unfollow')
            response = self.client.get('/users/admin/following')
            self.assertNotIn('abd', response.data)
 
        def test_followers_list(self):
            self.client.post(
                        '/users/login',
                        data = dict(username="admin",
                                    password="admin")
                        )
            self.client.get('/users/abd/follow')
            response = self.client.get('/users/abd/followers')
            self.assertIn('admin', response.data)

        def test_user_profile(self):
            self.client.post(
                        '/users/login',
                        data = dict(username="admin",
                                    password="admin")
                        )
            response1 = self.client.get('/users/abd/profile')
            response2 = self.client.get('/users/admin/profile')
            self.assertIn('From Abd', response1.data)
            self.assertIn('Testing Post', response2.data)

        def test_user_profile_has_no_posts_yet(self):
            with self.client:
                 self.client.post(
                        '/users/register',
                        data = dict(username="admino",
                                    email="admino@go.co",
                                    password="admino",
                                    confirm="admino")
                        )
            response = self.client.get('/users/admino/profile')
            self.assertIn('No Posts Yet', response.data)








if __name__ == '__main__':
    unittest.main()
