import os
import unittest
from coverage import Coverage
cov = Coverage(branch=True, omit=['*/.local/*', 'tests.py'])
cov.start()

from flask_testing import TestCase
from flask import abort, url_for

from app import create_app, db
from app.models import Post, User, Tag
from config import basedir


class TestBase(TestCase):

    def create_app(self):
        """
        Pass in test configs.
        """
        config_name = "config.TestingConfig"
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI="postgresql://ja:ja@localhost/posts_test"
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()

        # Create an admin
        admin = User(username='admin', password='admin', is_admin=True)

        # Create a simple user
        user = User(username='test_user', password='tester')

        # Create an unpublished post
        unpublished_post = Post(title='test_unpublished_post',
                                body='test-test-test')
        tags1 = Tag(tag_name='test, unpublished',
                    post=unpublished_post)

        # Create a published post
        published_post = Post(title='test_publised_post',
                              body='test-test-test-test',
                              publish=True)
        tags2 = Tag(tag_name='published, test',
                    post=published_post)

        insert = [admin,
                  user,
                  unpublished_post,
                  tags1,
                  published_post,
                  tags2]

        for i in insert:
            db.session.add(i)

        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()


class TestModels(TestBase):

    def test_user_model(self):
        '''
        Test number of records in User table
        '''
        self.assertEqual(User.query.count(), 2)

    def test_post_model(self):
        # create a post
        post = Post(title='example1',
                    body='blablabla')

        db.session.add(post)
        db.session.commit()

        self.assertEqual(Post.query.count(), 3)

    def test_tags_model(self):
        post = Post(title='example2',
                    body='blabla')
        tags = Tag(tag_name='something, this, that',
                   post=post)

        db.session.add(tags)
        db.session.commit()

        self.assertEqual(Tag.query.count(), 3)


class TestViews(TestBase):

    def test_index_view(self):
        '''
        Test that index page is accessible without login.
        '''
        response = self.client.get(url_for('home.index'))
        self.assertEqual(response.status_code, 200)

    def test_published_post_view(self):
        '''
        Test that a published post page is accessible without login.
        '''
        post = Post.query.filter_by(publish=True).first()
        response = self.client.get(url_for('home.post', id=post.id))
        self.assertEqual(response.status_code, 200)

    def test_unpublished_post_view(self):
        '''
        Test that a post page is innaccessible without login
        if post is unpublished.
        '''
        post = Post.query.filter_by(publish=False).first()
        response = self.client.get(url_for('home.post', id=post.id))
        self.assertEqual(response.status_code, 403)

    def test_search_tag_view(self):
        '''
        Test that the search-tag page is accessible.
        '''
        tag = Tag.query.first()
        tag = tag.tag_name.split(',')
        response = self.client.get(url_for('home.tag_search', tag=tag[0]))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        '''
        Test that login page is accessible without login.
        '''
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """
        Tests that logout is innaccessible without login
        and redirects to login page, then to logout.
        """
        target_url = url_for('auth.logout')
        redirect_url = url_for('home.index', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_dashboard_view(self):
        """
        Test that dashboard is innaccessible without login
        and redirects to login page, then to dashboard.
        """
        target_url = url_for('admin.dashboard')
        redirect_url = url_for('home.index', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


class TestErrorPages(TestBase):

    def test_403_forbidden(self):
        # create route to abort the request with the 403 error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue(b"403 Error" in response.data)

    def test_404_not_found(self):
        response = self.client.get('/nothinghere')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(b"404 Error" in response.data)

    def test_500_internal_server_error(self):
        # create route to abort the request with the 500 Error
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue(b"500 Error" in response.data)


if __name__ == "__main__":
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    print("HTML version: " + os.path.join(basedir, "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    cov.erase()
