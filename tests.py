import os
import unittest

from flask_testing import TestCase
from flask import abort, url_for

from app import create_app, db
from app.models import Post, User


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

        db.session.add(admin)
        db.session.add(user)
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
                    subtitle='blabla',
                    tags='x',
                    body='blablabla')

        db.session.add(post)
        db.session.commit()

        self.assertEqual(Post.query.count(), 1)


class TestViews(TestBase):

    def test_index_view(self):
        '''
        Test that index page is accessible without login.
        '''
        response = self.client.get(url_for('home.index'))
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
    unittest.main()
