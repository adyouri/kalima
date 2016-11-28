import unittest
import datetime
from flask_login import current_user
from base import BaseTestCase
from project.models import Comment, BlogPost, Category



class PostsTestCase(BaseTestCase):
        def test_index(self):
            response = self.client.get('/', content_type='html/text')
            self.assertEqual(response.status_code, 200)

        def test_404(self):
            response = self.client.get('/page_that_does_not_exist', content_type='html/text')
            self.assertIn('The page you requested does not exist', response.data)

        def test_500(self):
            response = self.client.get('/500', content_type='html/text')
            self.assertIn('Internal server error', response.data)

        def test_welcome(self):
            response = self.client.get('/posts/welcome', content_type='html/text')
            self.assertIn("welcome", response.data)

        def test_post_show_up(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = self.client.get('/posts/', follow_redirects=True)
            post = BlogPost.query.filter_by(id=3).first()
            self.assertTrue(str(post) == "<title From Abd | This is just a test post From Abd >")
            self.assertIn(b'From Abd', response.data)


        def test_latest_comments(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = self.client.get('/posts/', follow_redirects=True)
            self.assertIn(b'By', response.data)
            self.assertIn(b'In', response.data)

        def test_individual_post(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response1 = self.client.get('/posts/1', follow_redirects=True)
            response2 = self.client.get('/posts/2', follow_redirects=True)
            self.assertIn(b'This is just a test post', response2.data)
            self.assertIn(b'abd', response2.data)
            self.assertIn(b'This is just a test post to test tags', response2.data)
            self.assertIn(b'abd', response2.data)


        def test_post_has_comments(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = self.client.get('/posts/1', follow_redirects=True)
            comment = Comment.query.filter_by(id=1).first()
            self.assertTrue(str(comment) == "<Comment Test comment >")
            self.assertIn(b'admin', response.data)
            self.assertIn(b'Test comment', response.data)
            self.assertIn(b'abd', response.data)

        def test_comment_has_created_date(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            self.client.post(
                                    '/posts/1',
                                    data=dict(content="another comment here"),
                                    follow_redirects = True)

            response = self.client.get('/posts/1', follow_redirects=True)
            self.assertIn(b'just now', response.data) 
            self.assertIn(b'another comment here', response.data) 


        def test_post_has_no_comments(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = self.client.get('/posts/2', follow_redirects=True)
            self.assertIn(b'No comments yet', response.data)

        def test_post_in_category(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = self.client.get('/posts/cat/testing', follow_redirects=True)
            category = Category.query.filter_by(id=1).first()
            self.assertTrue(str(category) == "<name testing >")
            self.assertIn(b'Testing Post', response.data)

        def test_post_in_tag_page(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = self.client.get('/posts/tag/tests', follow_redirects=True)
            self.assertIn(b'Testing Tag', response.data)

        def test_page_not_found(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)

            response = self.client.get('/not_existing_page_or_user', follow_redirects=False)
            self.assertIn('The page you requested does not exist', response.data)

        def test_category_not_found(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)

            response = self.client.get('/posts/cat/not_existing_category', follow_redirects=False)
            self.assertIn('The page you requested does not exist', response.data)

        def test_category_has_no_posts(self):
            response = self.client.get("/posts/cat/testing_cat")
            self.assertIn('No Articles Yet.', response.data)

        def test_tag_not_found(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)

            response = self.client.get('/posts/tag/not_existing_tag', follow_redirects=False)
            self.assertIn('The page you requested does not exist', response.data)

        def test_add_post(self):
            with self.client:
                self.client.post(
                        '/users/login',
                        data=dict(username="admin", password="admin"),
                        follow_redirects = True)
                response = self.client.post(
                                        '/posts/new',
                                        data=dict(title="hello",
                                            description="This is a descriptio of the post",
                                            category="testing",
                                            ),
                                        follow_redirects = True)
                self.assertIn(b'hello', response.data)
                self.assertIn(b'/posts/cat/testing', response.data)
                self.assertIn(b'admin', response.data)
                self.assertTrue(current_user.name == "admin")
                self.assertTrue(current_user.is_active())

        def test_post_has_edit_button(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)

            response = self.client.get('/posts/1')
            self.assertIn('Edit', response.data)
            response2 = self.client.get('/posts/2')
            self.assertNotIn('Edit', response2.data)


        def test_edit_post(self):
            with self.client:
                response1 = self.client.get('/posts/1')
                self.assertIn(b"Testing Post", response1.data)
                self.client.post(
                        '/users/login',
                        data=dict(username="admin", password="admin"),
                        follow_redirects = True)
                response = self.client.post(
                                        '/posts/1/edit',
                                        data=dict(title="hello from admin",
                                            description="This is a description of the admin post",
                                            category="testing",
                                            tags = "testing_tag tagged_as_testing"
                                            ),
                                        follow_redirects = True)

                self.assertIn(b'hello from admin', response.data)
                self.assertIn(b'/posts/cat/testing', response.data)
                self.assertIn(b'/posts/tag/testing_tag', response.data)
                self.assertIn(b'/posts/tag/tagged_as_testing', response.data)
                self.assertTrue(current_user.name == "admin")
                self.assertTrue(current_user.is_active())
                response2 = self.client.get('/posts/1')
                self.assertIn(b"This is a description of the admin post", response2.data)

        def test_delete_post(self):
            with self.client:
                self.client.post(
                        '/users/login',
                        data=dict(username="admin", password="admin"),
                        follow_redirects = True)
                response = self.client.post(
                                 '/posts/new',
                                 data=dict(title="to be deleted",
                                     description="This post will be deleted",
                                     category="deleting",
                                     tags="deleting1 deleting2 deleting3",
                                     ),
                                 follow_redirects = True)
                post = BlogPost.query.filter(BlogPost.title=='to be deleted').first()
                self.assertTrue(post.description == 'This post will be deleted')
                self.assertTrue(post.category.name == 'deleting')
                response = self.client.get('/posts/cat/deleting')
                self.assertIn(b'to be deleted', response.data)

                # delete it
                self.client.get('/posts/{}/delete'.format(post.id))
                post = BlogPost.query.filter_by(title='to be deleted').first()
                self.assertFalse(post)
                response = self.client.get('/posts/cat/deleting')
                self.assertNotIn(b'to be deleted', response.data)

        def test_post_has_delete_button(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)

            response = self.client.get('/posts/1', follow_redirects=True)
            self.assertIn('Delete', response.data)
            response2 = self.client.get('/posts/2', follow_redirects=True)
            self.assertNotIn('Delete', response2.data)


        def test_user_cannot_delete_other_posts(self):
            with self.client:
                self.client.post(
                        '/users/login',
                        data=dict(username="admin", password="admin"),
                        follow_redirects = True)
                response = self.client.post(
                                 '/posts/new',
                                 data=dict(title="to be deleted",
                                     description="This post will be deleted",
                                     category="deleting",
                                     tags="deleting1 deleting2 deleting3",
                                     ),
                                 follow_redirects = True)
                post = BlogPost.query.filter(BlogPost.title=='to be deleted').first()
                self.assertTrue(post.description == 'This post will be deleted')
                self.assertTrue(post.category.name == 'deleting')
                response = self.client.get('/posts/cat/deleting')
                self.assertIn(b'to be deleted', response.data)

                # log out

                self.client.get('/users/logout', follow_redirects=True)

                # login another user
                self.client.post(
                        '/users/login',
                        data=dict(username="abd", password="abd"),
                        follow_redirects = True)

                # delete it
                response1 = self.client.get('/posts/{}/delete'.format(post.id), follow_redirects=True)
                self.assertIn(b'You cannot delete this post', response1.data)
                post = BlogPost.query.filter_by(title='to be deleted').first()
                self.assertTrue(post)
                response2 = self.client.get('/posts/cat/deleting')
                self.assertIn(b'to be deleted', response2.data)


                




        def test_post_date(self):

            with self.client:
                self.client.post(
                        '/users/login',
                        data=dict(username="admin", password="admin"),
                        follow_redirects = True)
                response = self.client.post(
                                        '/posts/new',
                                        data=dict(title="hello date",
                                            description="Description For Date Post",
                                            category="testing",
                                            tags = "testing test tag_test"
                                            ),
                                        follow_redirects = True)
                self.assertIn(b'hello', response.data)
                self.assertIn(b'/posts/cat/testing', response.data)
                self.assertIn(b'admin', response.data)
                self.assertIn(str(datetime.datetime.utcnow().date()), response.data)
                self.assertIn(b'just now', response.data)
                self.assertTrue(current_user.name == "admin")
                self.assertTrue(current_user.is_active())


        def test_correct_add_comment_to_post(self):

            with self.client:
                self.client.post(
                        '/users/login',
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
                        '/users/login',
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
                        '/users/login',
                        data=dict(username="abd", password="abd"),
                        follow_redirects = True)
                response = self.client.post(
                                        '/posts/new',
                                        data=dict(title="hello",
                                            description="post with new category",
                                            category="new_category",
                                            tags="tag0 tag1 tag2",
                                            ),
                                        follow_redirects = True)
                self.assertIn(b'hello', response.data)
                self.assertIn(b'/posts/cat/new_category', response.data)
                self.assertIn(b'tag0', response.data)
                self.assertIn(b'tag1', response.data)
                self.assertIn(b'tag2', response.data)
                self.assertTrue(current_user.name == "abd")
        def test_tag_has_posts(self):
            with self.client:
                self.client.post(
                        '/users/login',
                        data=dict(username="abd", password="abd"),
                        follow_redirects = True)
                self.client.post(
                                        '/posts/new',
                                        data=dict(title="hello",
                                            description="post with new category",
                                            category="new_category",
                                            tags="tag0 tag1 tag2",
                                            ),
                                        follow_redirects = True)

                self.client.post(
                                        '/posts/new',
                                        data=dict(title="Hello2",
                                            description="post with tag0",
                                            category="new_category",
                                            tags="tag0",
                                            ), follow_redirects=True)
                response = self.client.get('/posts/tag/tag0')
                self.assertIn(b'Hello2', response.data)
                self.assertIn(b'hello', response.data)

        def test_incorrect_add_post(self):
            with self.client:
                response = self.client.post(
                                        '/posts/new',
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

        def test_add_favorite(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = self.client.get('/posts/2/fav', follow_redirects=True)
            self.assertIn(b'"status": 200', response.data)

        def test_user_can_only_edit_his_posts(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response1 = self.client.get('/posts/1/edit', follow_redirects=True)
            response2 = self.client.get('/posts/3/edit', follow_redirects=True)
            self.assertIn(b'Edit Post:', response1.data)
            self.assertNotIn(b'Edit Post:', response2.data)
            self.assertIn(b'Post is not yours', response2.data)



        def test_remove_from_favorites(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = self.client.get('/posts/2/fav', follow_redirects=True)
            self.assertIn(b'"status": 200', response.data)
            response2 = self.client.get('/posts/2/unfav', follow_redirects = True)
            self.assertIn(b'"status": 200', response2.data)
 
            
        def test_favorites_page(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            response = self.client.get('/users/admin/favorites', follow_redirects=True)
            self.assertIn(b'Testing Post', response.data)

        def test_favorited_post_has_fav_users_list(self):
            self.client.post(
                    '/users/login',
                    data=dict(username="abd", password="abd"),
                    follow_redirects=True)
            self.client.get('/posts/1/fav', follow_redirects=True)
            response = self.client.get('/posts/1', follow_redirects=True)
            self.assertIn(b'<li>abd</li>', response.data)


        def test_fav_users_api_list(self):
            self.client.post(
                                    '/users/login',
                                    data=dict(username="admin", password="admin"),
                                    follow_redirects = True)
            self.client.get('/posts/1/fav', follow_redirects=True)
            response = self.client.get('/posts/1/fav_users')
            self.assertIn(b'admin', response.data)

        def test_user_cannot_access_others_private_favorites(self):

            self.client.post(
                    '/users/login',
                    data=dict(username="abd", password="abd"),
                    follow_redirects=True)
            response = self.client.get('/users/admin/favorites', follow_redirects=True)
            self.assertIn(b'You cannot access this page', response.data)


        def test_user_can_access_his_private_favorites(self):
            self.client.post(
                    '/users/login',
                    data=dict(username="admin", password="admin"),
                    follow_redirects=True)
            response = self.client.get('/users/admin/favorites', follow_redirects=True)
            self.assertIn(b'Testing Post', response.data)



if __name__ == '__main__':
    unittest.main()
