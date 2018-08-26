import unittest

from flask import current_app
from app.create_app import create_app


class TestDevelopmentConfig(unittest.TestCase):
    app = create_app('development')

    def test_app_is_development(self):

        """
            Test the Development Environment Configuration
        """

        self.assertFalse(self.app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(self.app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)


class TestTestingConfig(unittest.TestCase):

    """
        Test the Testing Environment Configuratin
    """

    app = create_app('testing')

    def test_app_is_testing(self):
        self.assertFalse(self.app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(self.app.config['DEBUG'])
        self.assertTrue(self.app.config['TESTING'])


class TestProductionConfig(unittest.TestCase):
    """
        Test the Production Environment Configuratin
    """

    app = create_app('production')

    def test_app_is_production(self):
        self.assertTrue(self.app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
