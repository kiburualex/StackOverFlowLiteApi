import unittest
import json
from .base import BaseTestCase
from app.modules.user.models import User


class TestUserAuthentication(BaseTestCase):
    endpoint = 'api/v1/users/'

    def test_encode_auth_token(self):

        """ Test encoding authentication token """

        """
            GET Request
        """
        response = self.client.get(self.endpoint + '1/', headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)

        """
            Convert content extract data
        """
        content = json.loads(response.get_data(as_text=True))

        """
            Encode data to generate token
        """
        auth_token = User().encode_auth_token(content['email'])
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):

        """ Test decoding authentication token """

        """
            GET Request
        """
        response = self.client.get(self.endpoint + '1/', headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)

        """
            Convert content extract data
        """
        content = json.loads(response.get_data(as_text=True))

        """
            Decode data to generate token
        """
        auth_token = User().encode_auth_token(content['email'])

        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(type(User().decode_auth_token(auth_token.decode("utf-8"))) == int)

    def test_registered_user_login(self):

        """ Test for login of registered-user login """

        """
            Context Manager to execute multiple statements together
        """
        with self.client:
            """
                Initial user registration
            """
            user = {
                "username": "Alex Kiburu",
                "email": "alex@example.com",
                "password": "alex123",
                "role": "customer"
            }

            user_response = self.client.post('api/v1/auth/signup/',
                                             data=json.dumps(user),
                                             content_type='application/json')

            response_data = json.loads(user_response.data.decode())

            self.assertEqual(user_response.status_code, 201)
            self.assertTrue(response_data[0]['Authorization'])

            """
             Initial registered user login
            """
            login_response = self.client.post('api/v1/auth/login/',
                                              data=json.dumps(
                                                  {
                                                      "email": user['email'],
                                                      "password": user['password']
                                                   }
                                              ),
                                              content_type='application/json')
            data = json.loads(login_response.data.decode())

            self.assertEqual(login_response.status_code, 200)
            self.assertTrue(data['Authorization'])

    def test_valid_logout(self):

        """ Test for logout before token expires """

        """
            Context Manager to execute multiple statements together
        """
        with self.client:
            """
                Initial user registration
            """
            user = {
                "username": "Alex Kiburu",
                "email": "alex@example.com",
                "password": "alex123",
                "role": "customer"
            }
            user_response = self.client.post('api/v1/auth/signup/',
                                             data=json.dumps(user),
                                             content_type='application/json')
            response_data = json.loads(user_response.data.decode())

            self.assertTrue(response_data[0]['Authorization'])
            self.assertEqual(user_response.status_code, 201)

            """
                valid token logout
            """
            response = self.client.post(
                'api/v1/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        user_response.data.decode()
                    )[0]['Authorization']
                )
            )

            data = json.loads(response.data.decode())

            self.assertTrue(data['status'] == 'success')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
