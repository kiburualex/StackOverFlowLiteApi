import unittest
import json

from .base import BaseTestCase

class UserTestCase(BaseTestCase):

    endpoint = 'api/v1/users/'

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
        response = self.client.get(self.endpoint + '1/')
        self.assertEqual(response.status_code, 200)

    def test_user_can_be_edited(self):
        """Test API can edit an existing user. (PUT request)"""

        user = {
            'id': 1,
            'name': 'Alex Kiburu',
            'email': 'alexkiburu18@gmail.com',
            'password': 'saf&&#d12'
        }
        response = self.client.put(self.endpoint + '1/',
                                    data=json.dumps(user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        results = self.client.get(self.endpoint + '1/')

        content = json.loads(results.get_data(as_text=True))
        self.assertEqual(content, user)


    def test_register_user(self):
        """Test API can create a user (POST request)"""
        user = {
            'id': 1,
            'name': 'Alex Kiburu',
            'email': 'alexkiburu18@gmail.com',
            'password': 'saf&&#d12'
        }
        response = self.client.post(self.endpoint,
                                    data=json.dumps(user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')

        content = json.loads(response.get_data(as_text=True))
        self.assertEqual(content, user)


if __name__ == '__main__':
    unittest.main()
