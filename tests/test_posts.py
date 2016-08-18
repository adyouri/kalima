import unittest
import datetime
from flask_login import current_user
from base import BaseTestCase
from project.models import Comment, BlogPost, Category



class PostsTestCase(BaseTestCase):
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
            post = BlogPost.query.filter_by(id=2).first()
            self.assertTrue(str(post) == "<title From Abd | This is just a test post From Abd >")
            self.assertIn(b'From Abd', response.data)

        def test_individual_post(self):
            self.client.post(
                                    '/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response1 = self.client.get('/posts/1', follow_redirects=True)
            response2 = self.client.get('/posts/2', follow_redirects=True)
            self.assertIn(b'This is just a test post', response2.data)
            self.assertIn(b'admin', response2.data)
            self.assertIn(b'This is just a test post From Abd', response2.data)
            self.assertIn(b'abd', response2.data)


        def test_post_has_comments(self):
            self.client.post(
                                    '/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = self.client.get('/posts/1', follow_redirects=True)
            comment = Comment.query.filter_by(id=1).first()
            self.assertTrue(str(comment) == "<Comment Test comment >")
            self.assertIn(b'admin', response.data)
            self.assertIn(b'Test comment', response.data)
            self.assertIn(b'abd', response.data)

        def test_post_has_no_comments(self):
            self.client.post(
                                    '/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = self.client.get('/posts/2', follow_redirects=True)
            self.assertIn(b'No comments yet', response.data)



        def test_post_in_category(self):
            self.client.post(
                                    '/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = self.client.get('/cat/testing', follow_redirects=True)
            category = Category.query.filter_by(id=1).first()
            self.assertTrue(str(category) == "<name testing >")
            self.assertIn(b'Testing Post', response.data)

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

        def test_add_post(self):

            with self.client:
                self.client.post(
                        '/login',
                        data=dict(username="admin", password="admin"),
                        follow_redirects = True)
                response = self.client.post(
                                        '/add_post',
                                        data=dict(title="hello",
                                            description="This is a descriptio of the post",
                                            category="testing",
                                            ),
                                        follow_redirects = True)
                self.assertIn(b'hello', response.data)
                self.assertIn(b'/cat/testing', response.data)
                self.assertIn(b'admin', response.data)
                self.assertTrue(current_user.name == "admin")
                self.assertTrue(current_user.is_active())

        def test_post_date(self):

            with self.client:
                self.client.post(
                        '/login',
                        data=dict(username="admin", password="admin"),
                        follow_redirects = True)
                response = self.client.post(
                                        '/add_post',
                                        data=dict(title="hello date",
                                            description="Description For Date Post",
                                            category="testing",
                                            ),
                                        follow_redirects = True)
                self.assertIn(b'hello', response.data)
                self.assertIn(b'/cat/testing', response.data)
                self.assertIn(b'admin', response.data)
                self.assertIn(str(datetime.datetime.utcnow().date()), response.data)
                self.assertIn(b'seconds ago', response.data)
                self.assertTrue(current_user.name == "admin")
                self.assertTrue(current_user.is_active())


        def test_correct_add_comment_to_post(self):

            with self.client:
                self.client.post(
                        '/login',
                        data=dict(username="admin", password="admin"),
                        follow_redirects = True)
                response = self.client.post(
                                        '/posts/1',
                                        data=dict(content="test comment",
                                            ),
                                        follow_redirects = True)
                self.assertIn(b'Added new comment successfully!', response.data)
                self.assertIn(b'test comment', response.data)
                self.assertIn(b'admin', response.data)
                self.assertTrue(current_user.name == "admin")
                self.assertTrue(current_user.is_active())

        def test_incorrect_add_comment_to_post(self):

            with self.client:
                self.client.post(
                        '/login',
                        data=dict(username="admin", password="admin"),
                        follow_redirects = True)
                response = self.client.post(
                                        '/posts/2',
                                        data=dict(content="",
                                            ),
                                        follow_redirects = True)
                self.assertIn(b'field is required', response.data)



        def test_add_category(self):

            with self.client:
                self.client.post(
                        '/login',
                        data=dict(username="abd", password="abd"),
                        follow_redirects = True)
                response = self.client.post(
                                        '/add_post',
                                        data=dict(title="hello",
                                            description="post with new category",
                                            category="new_category",
                                            ),
                                        follow_redirects = True)
                self.assertIn(b'hello', response.data)
                self.assertIn(b'/cat/new_category', response.data)
                self.assertIn(b'abd', response.data)
                self.assertTrue(current_user.name == "abd")
                self.assertTrue(current_user.is_active())

        def test_incorrect_add_post(self):
            with self.client:
                response = self.client.post(
                                        '/add_post',
                                        data=dict(title="""
                                                            Too much characters in the title
                                                            Too much characters in the title
                                                            Too much characters in the title
                                                            Too much characters in the title
                                                        """,
                                            description="",
                                            category="new_category",
                                            ),
                                        follow_redirects = True)
                self.assertIn(b'Field cannot be longer than 100 characters.', response.data)
                self.assertIn(b'This field is required.', response.data)


if __name__ == '__main__':
    unittest.main()
