from project import app
import unittest

class FlaskTestCase(unittest.TestCase):
        def test_index(self):
            tester = app.test_client(self)
            response = tester.get('/login', content_type='html/text')
            self.assertEqual(response.status_code, 200)

        def test_login_page_loads(self):
            tester = app.test_client(self)
            response = tester.get('/login', content_type='html/text')
            self.assertTrue(b'Please login' in response.data)

        def test_correct_login(self):
            tester = app.test_client(self)
            response = tester.post(
                                    '/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            self.assertIn(b'You were logged in', response.data)
        def test_incorrect_login(self):
            tester = app.test_client(self)
            response = tester.post(
                                    '/login',
                                    data=dict(username="wrong", password="admin"),
                                    follow_redirects = True)
            self.assertIn(b'Invalid', response.data)
        def test_logout(self):
            tester = app.test_client(self)
            tester.post(
                                    '/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = tester.get('/logout', follow_redirects=True)
            self.assertIn(b'Please login', response.data)

        def test_main_route_requires_login(self):
            tester = app.test_client(self)
            response = tester.get('/', follow_redirects=True)
            self.assertIn(b'Please login', response.data)

        def test_post_show_up(self):
            tester = app.test_client(self)
            tester.post(
                                    '/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = tester.get('/', follow_redirects=True)
            self.assertIn(b'Well', response.data)

        def test_post_in_category(self):
            tester = app.test_client(self)
            tester.post(
                                    '/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = tester.get('/cat/freelancing', follow_redirects=True)
            self.assertIn(b'Ahlan World', response.data)

        def test_post_by_author(self):
            tester = app.test_client(self)
            tester.post(
                                    '/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = tester.get('/u/abd', follow_redirects=True)
            response1 = tester.get('/admin', follow_redirects=True)
            response2 = tester.get('/user/admin', follow_redirects=True)
            self.assertIn(b'From Abd', response.data)
            self.assertIn(b'good', response1.data)
            self.assertIn(b'well', response2.data)

        def test_page_not_found(self):
            tester = app.test_client(self)
            tester.post(
                                    '/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)

            response = tester.get('/not_existing_page_or_user', follow_redirects=False)
            self.assertEqual(response.status_code, 404)

        def test_category_not_found(self):
            tester = app.test_client(self)
            tester.post(
                                    '/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)

            response = tester.get('/cat/not_existing_category', follow_redirects=False)
            self.assertEqual(response.status_code, 404)
        def test_user_not_found(self):
            tester = app.test_client(self)
            tester.post(
                                    '/login',
                                    data=dict(
                                        username="admin",
                                        password="admin"),
                                        follow_redirects = True)

            response = tester.get('/u/not_existing_user', follow_redirects=False)
            response1 = tester.get('/user/not_existing_user', follow_redirects=False)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response1.status_code, 404)






if __name__ == '__main__':
    unittest.main()
