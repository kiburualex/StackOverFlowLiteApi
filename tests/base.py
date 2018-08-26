import unittest
import json
from app.create_app import create_app
from app.migrations.db import db


class BaseTestCase(unittest.TestCase):

    """ Base Test case class, initialize variables and settings """

    def setUp(self):

        """Define test variables and initialize app."""

        """ create the database and the tables """
        db.migrate_test_db()

        self.app = create_app("testing")
        self.client = self.app.test_client()

        question = {
            "title": "Build an API",
            "body": "How does one build an api"
        }

        user = {
            "username": "Alex Kiburu",
            "email": "admin@example.com",
            "password": "admin123",
            "role": "customer"
        }

        """ lambda functions to return responses """
        self.signup_user = lambda x=None: self.client.post('api/v1/auth/signup/',
                                                           data=json.dumps(user),
                                                           content_type='application/json')

        self.post_one_question = lambda auth_headers: self.client.post('api/v1/questions/',
                                                                       data=json.dumps(question),
                                                                       content_type='application/json',
                                                                       headers=auth_headers)

        """
            required: signup user to get the user to be used in asking
                      questions and gaining token to access other urls
            Initial user registration and login
        """
        signed_up_user = self.signup_user()

        print(signed_up_user)

        """
            Header with Authorization token from logged in user above
        """
        self.auth_headers = dict(
            Authorization=json.loads(
                signed_up_user.data.decode())[0]['Authorization']
        )

        """
            Create an initial question
            @:param ( Authorization token )

        """
        self.post_one_question(self.auth_headers)

    def tearDown(self):

        """ drop the database """

        db.drop_test_database()
