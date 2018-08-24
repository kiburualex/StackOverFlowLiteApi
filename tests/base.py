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
            "id": 1,
            "title": "Build an API",
            "body": "How does one build an api",
            "user_id": 1
        }

        user = {
            "id": 1,
            "username": "Alex Kiburu",
            "email": "admin@example.com",
            "password": "admin123",
            "role": "customer"
        }

        user_login = {
            "email": "admin@example.com",
            "password": "admin123"
        }

        """ lambda functions to return responses """
        self.signup_user = lambda x=None: self.client.post('api/v1/auth/signup/',
                                                           data=json.dumps(user),
                                                           content_type='application/json')

        self.user_login = lambda x=None: self.client.post('api/v1/auth/login/',
                                                          data=json.dumps(user_login),
                                                          content_type='application/json')

        self.post_one_question = lambda auth_headers: self.client.post('api/v1/questions/',
                                                                       data=json.dumps(question),
                                                                       content_type='application/json',
                                                                       headers=auth_headers)

    def tearDown(self):

        """ drop the database """
        db.drop_test_database()
