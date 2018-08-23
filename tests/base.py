import unittest
import json
from app.create_app import create_app


class BaseTestCase(unittest.TestCase):
    """ Base Test case class, initialize variables and settings """

    def setUp(self):
        """Define test variables and initialize app."""
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
            "email": "alexkiburu18@gmail.com",
            "password": "saf&&#d12",
            "role": "customer"
        }

        self.post_one_user = lambda x=None: self.client.post('api/v1/users/',
                                                             data=json.dumps(user),
                                                             content_type='application/json')
        self.post_one_question = lambda x=None: self.client.post('api/v1/questions/',
                                                                 data=json.dumps(question),
                                                                 content_type='application/json')

    def tearDown(self):
        """ drop all the test database """
        pass
