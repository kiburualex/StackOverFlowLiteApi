import unittest
import json

from .base import BaseTestCase


class UserTestCase(BaseTestCase):

    endpoint = 'api/v1/users/'

    def test_api_can_get_all_list_users(self):

        """ Test API can get all users (GET request). """

        """
            Initial user registration and login
        """
        # self.signup_user()
        # login_response = self.user_login()

        """
            Header with Authorization token from logged in user above
        """
        # auth_headers = dict(
        #     Authorization=json.loads(
        #         login_response.data.decode())['Authorization']
        # )

        response = self.client.get(self.endpoint, headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_api_can_get_user_by_id(self):

        """ Test API can get a single user by using it's id. """

        """
            Initial user registration and login
        """
        # self.signup_user()
        # login_response = self.user_login()

        """
            Header with Authorization token from logged in user above
        """
        # auth_headers = dict(
        #     Authorization=json.loads(
        #         login_response.data.decode())['Authorization']
        # )

        response = self.client.get(self.endpoint + '1/', headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_error_status_on_not_found_user_id(self):

        """ Test a 404 error when user id is not found. """

        """
            Initial user registration and login
        """
        # self.signup_user()
        # login_response = self.user_login()

        """
            Header with Authorization token from logged in user above
        """
        # auth_headers = dict(
        #     Authorization=json.loads(
        #         login_response.data.decode())['Authorization']
        # )

        response = self.client.get(self.endpoint + '100/', headers=self.auth_headers)
        self.assertEqual(response.status_code, 404)

    def test_user_can_be_edited(self):

        """ Test API can edit an existing user. (PUT request) """

        """
            Initial user registration and login
        """
        # self.signup_user()
        # login_response = self.user_login()

        """
            Header with Authorization token from logged in user above
        """
        # auth_headers = dict(
        #     Authorization=json.loads(
        #         login_response.data.decode())['Authorization']
        # )

        user = {
            "id": 1,
            "username": "Alex Kiburu",
            "email": "alexkiburu18@gmail.com",
            "password": "saf&&#d12",
            "role": "customer"
        }

        response = self.client.put(self.endpoint + '1/',
                                   data=json.dumps(user),
                                   content_type='application/json',
                                   headers=self.auth_headers)

        self.assertEqual(response.status_code, 200)
        results = self.client.get(self.endpoint + '1/', headers=self.auth_headers)

        content = json.loads(results.get_data(as_text=True))
        self.assertEqual(content['email'], user['email'])

    def test_register_user(self):

        """ Test API can create a user (POST request) """

        """
            Initial user registration and login
        """
        # self.signup_user()
        # login_response = self.user_login()

        """
            Header with Authorization token from logged in user above
        """
        # auth_headers = dict(
        #     Authorization=json.loads(
        #         login_response.data.decode())['Authorization']
        # )

        user = {
            "id": 1,
            "username": "Alex Kiburu",
            "email": "alexkiburu18@gmail.com",
            "password": "saf&&#d12",
            "role": "customer"
        }

        response = self.client.post(self.endpoint,
                                    data=json.dumps(user),
                                    content_type='application/json',
                                    headers=self.auth_headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')


if __name__ == '__main__':
    unittest.main()
