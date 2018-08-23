import unittest
import json

from .base import BaseTestCase

class UserTestCase(BaseTestCase):

    endpoint = 'api/v1/users/'

    def create_one_user(self):
        user = {
            "id": 1,
            "username": "Alex Kiburu",
            "email": "alexkiburu18@gmail.com",
            "password": "saf&&#d12",
            "role": "customer"
        }
        self.client.post(self.endpoint,
                         data=json.dumps(user),
                         content_type='application/json')

    def test_home_status_code(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)

    def test_api_can_get_all_list_users(self):
        """Test API can get all users (GET request)."""
        response = self.client.get(self.endpoint)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_api_can_get_user_by_id(self):
        """Test API can get a single user by using it's id."""
        self.post_one_user()
        response = self.client.get(self.endpoint + '1/')
        self.assertEqual(response.status_code, 200)

    def test_error_status_on_not_found_user_id(self):
        """Test a 404 error when user id is not found."""
        response = self.client.get(self.endpoint + '100/')
        self.assertEqual(response.status_code, 404)

    def test_user_can_be_edited(self):
        """Test API can edit an existing user. (PUT request)"""
        self.post_one_user()

        user = {
            "id": 1,
            "username": "Alex Kiburu",
            "email": "alexkiburu18@gmail.com",
            "password": "saf&&#d12",
            "role": "customer"
        }
        response = self.client.put(self.endpoint + '1/',
                                    data=json.dumps(user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        results = self.client.get(self.endpoint + '1/')

        content = json.loads(results.get_data(as_text=True))
        self.assertEqual(content['email'], user['email'])

    def test_register_user(self):
        """Test API can create a user (POST request)"""
        user = {
            "id": 1,
            "username": "Alex Kiburu",
            "email": "alexkiburu18@gmail.com",
            "password": "saf&&#d12",
            "role": "customer"
        }
        response = self.client.post(self.endpoint,
                                    data=json.dumps(user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')


if __name__ == '__main__':
    unittest.main()