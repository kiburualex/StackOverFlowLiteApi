import unittest

from app.api.v1 import api
from app.api.v1.question import ns as questions_namespace
from app.api.v1.user import ns as users_namespace
from config import create_app


""" Base Test case class, initialize variables and settings """
class BaseTestCase(unittest.TestCase):
    """A base test case."""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("testing")

        api.init_app(self.app)
        api.add_namespace(questions_namespace)
        api.add_namespace(users_namespace)

        self.client = self.app.test_client()