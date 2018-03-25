"""
The testing module of the application.
Contains test cases for the available
endpoints.
"""

import unittest
from mock import patch, Mock

from flask import jsonify
from flask_testing import TestCase

from main import app, db, twitter_api, NUMBER_OF_POSTS
import models

# Some setup objects to avoid querying the actual Twitter API in each test
USERS_COUNT = 5
stream_sample = twitter_api.GetStreamSample()
random_users = []
while len(random_users) < USERS_COUNT:
    try:
        random_users.append(stream_sample.next()['user'])
    except KeyError:
        pass
random_user_id = random_users[0]['id']
random_user_statuses = twitter_api.GetUserTimeline(user_id=random_user_id, count=NUMBER_OF_POSTS)


def add_users():
    """Helpful method to add users to the database whenever needed"""
    db.session.add_all([models.User(random_user) for random_user in random_users])
    db.session.commit()


class RoutesTest(TestCase):
    """Testing class for the available routes"""

    def create_app(self):
        """Creates the app to be tested"""
        app.config['TESTING'] = True
        return app

    def setUp(self):
        """The setup function that runs before each test"""
        db.create_all()

    def tearDown(self):
        """The tear down function that runs after each test"""
        db.session.remove()
        db.drop_all()

    def test_all_users(self):
        """Test cases for the '/users/' endpoint"""
        self.assertEqual(self.client.get("/users/").json, [])
        add_users()
        self.assertTrue(self.client.get("/users/").json
                        <= jsonify([dict(user) for user in models.User.query.all()]).json)

    @patch('routes.twitter_api')
    def test_user_data(self, fake_api):
        """Test cases for the '/users/<twitter_id>/' endpoint"""

        fake_user = Mock()
        fake_user.AsDict = Mock(return_value=random_users[0])
        fake_api.GetUser = Mock(return_value=fake_user)

        self.assert404(self.client.get("/users/invalid_id/"))
        fake_api.GetUser.assert_not_called()
        fake_user.AsDict.assert_not_called()

        self.assert404(self.client.get("/users/{}/?local=true".format(random_user_id)))
        fake_api.GetUser.assert_not_called()
        fake_user.AsDict.assert_not_called()

        self.assertEqual(self.client.get("/users/{}/".format(random_user_id)).json,
                         jsonify(dict(models.User.query.get(random_user_id))).json)
        fake_api.GetUser.assert_called_with(user_id=unicode(random_user_id))
        fake_user.AsDict.assert_called()

        fake_api.GetUser.reset_mock()
        fake_user.AsDict.reset_mock()

        self.assertEqual(self.client.get("/users/{}/?local=true".format(random_user_id)).json,
                         jsonify(dict(models.User.query.get(random_user_id))).json)
        fake_api.GetUser.assert_not_called()
        fake_user.AsDict.assert_not_called()

    @patch('routes.twitter_api')
    def test_user_posts(self, fake_api):
        """Test cases for the '/users/<twitter_id>/posts/' endpoint"""

        fake_user = Mock()
        fake_user.AsDict = Mock(return_value=random_users[0])
        fake_api.GetUser = Mock(return_value=fake_user)
        fake_api.GetUserTimeline = Mock(return_value=random_user_statuses)

        self.assert404(self.client.get("/users/invalid_id/posts/"))
        fake_api.GetUser.assert_not_called()
        fake_user.AsDict.assert_not_called()

        self.assert404(self.client.get("/users/{}/posts/?local=true".format(random_user_id)))
        fake_api.GetUser.assert_not_called()
        fake_user.AsDict.assert_not_called()

        self.assertTrue(self.client.get("/users/{}/posts/".format(random_user_id)).json
                        <= jsonify([dict(status) for status in models.Status.query.all()]).json)
        fake_api.GetUser.assert_called_with(user_id=unicode(random_user_id))
        fake_user.AsDict.assert_called()

        fake_api.GetUser.reset_mock()
        fake_user.AsDict.reset_mock()

        self.assertTrue(self.client.get("/users/{}/posts/?local=true".format(random_user_id)).json
                        <= jsonify([dict(status) for status in models.Status.query.all()]).json)
        fake_api.GetUser.assert_not_called()
        fake_user.AsDict.assert_not_called()


if __name__ == '__main__':
    unittest.main()
