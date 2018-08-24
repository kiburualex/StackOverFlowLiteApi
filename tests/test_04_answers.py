import unittest
import json

from .base import BaseTestCase


class AnswerTestCase(BaseTestCase):

    endpoint = 'api/v1/questions/'

    def test_post_answer(self):

        """ Test API can create a an Answer """

        """
            Initial user registration and login
        """
        self.signup_user()
        login_response = self.user_login()

        """
            Header with Authorization token from logged in user above
        """
        auth_headers = dict(
            Authorization=json.loads(
                login_response.data.decode())['Authorization']
        )

        """
            Create an initial question
            @:param ( users_id, Authorization token )
        """
        self.post_one_question(auth_headers)

        """ 
            Simulate answer creation
        """
        answer = {
            "id": 1,
            "user_id": 1,
            "question_id": 1,
            "answer_body": "Sample Answer"
        }
        answer_response = self.client.post(self.endpoint + '1/answers',
                                           data=json.dumps(answer),
                                           content_type='application/json',
                                           headers=auth_headers)
        self.assertEqual(answer_response.status_code, 201)

    def test_post_answer_with_incorrect_inputs(self):

        """ Test API post Answer with incorrect input data """

        """
            Initial user registration and login
        """
        self.signup_user()
        login_response = self.user_login()

        """
            Header with Authorization token from logged in user above
        """
        auth_headers = dict(
            Authorization=json.loads(
                login_response.data.decode())['Authorization']
        )
        self.post_one_question(auth_headers)

        """ 
            Simulate answer creation
        """
        answer = {
            'id': 1,
            'answer_body': '',
            'user_id': ' '
        }
        answer_response = self.client.post(self.endpoint + '1/answers',
                                           data=json.dumps(answer),
                                           content_type='application/json',
                                           headers=auth_headers)
        self.assertEqual(answer_response.status_code, 400)

        answer_content = json.loads(answer_response.get_data(as_text=True))
        self.assertEqual(answer_content['message'], "Incorrect Data Format. Try again")

    def test_api_can_get_answers_of_a_question_by_question_id(self):

        """ Test API can get answers of question by question id. """

        """
            Initial user registration and login
        """
        self.signup_user()
        login_response = self.user_login()

        """
            Header with Authorization token from logged in user above
        """
        auth_headers = dict(
            Authorization=json.loads(
                login_response.data.decode())['Authorization']
        )

        """
            Create an initial question
            @:param ( users_id, Authorization token )
        """
        self.post_one_question(auth_headers)

        """
            GET request
        """
        response = self.client.get(self.endpoint + '1/answers', headers=auth_headers)
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.get_data(as_text=True))

        """ assert if answers response is a list """
        self.assertIsInstance(content, list)

    def test_api_can_get_answers_of_non_existing_id(self):

        """ Test API can get answers of question by question id. """

        """
            Initial user registration and login
        """
        self.signup_user()
        login_response = self.user_login()

        """
            Header with Authorization token from logged in user above
        """
        auth_headers = dict(
            Authorization=json.loads(
                login_response.data.decode())['Authorization']
        )

        """
            Create an initial question
            @:param ( users_id, Authorization token )

        """
        self.post_one_question(auth_headers)

        """
            GET request
        """
        response = self.client.get(self.endpoint + '100/answers', headers=auth_headers)
        self.assertEqual(response.status_code, 404)

        content = json.loads(response.get_data(as_text=True))
        self.assertEqual(content['message'], "Question 100 doesn't exist")


if __name__ == '__main__':
    unittest.main()
