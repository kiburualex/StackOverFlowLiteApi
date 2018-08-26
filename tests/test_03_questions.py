import unittest
import json

from .base import BaseTestCase


class QuestionTestCase(BaseTestCase):

    endpoint = 'api/v1/questions/'

    def test_home_status_code(self):

        """ Test connection of home route """

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)

    def test_api_can_get_all_list_questions(self):

        """ Test API can get all questions (GET request). """

        """
            GET request
        """
        response = self.client.get(self.endpoint, headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_api_can_get_question_by_id(self):

        """ Test API can get a single question by using it's id. """

        """
            GET request
        """
        # self.post_one_question(auth_headers)
        response = self.client.get(self.endpoint + '1/', headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_error_status_on_not_found_question_id(self):

        """ Test a 404 error when question id is not found. """

        response = self.client.get(self.endpoint + '100/', headers=self.auth_headers)
        self.assertEqual(response.status_code, 404)

    def test_question_can_be_edited(self):

        """ Test API can edit an existing question. (PUT request) """

        question = {
            "id": 1,
            "title": "Build an API",
            "body": "How does one build an api",
            "user_id": 1
        }

        response = self.client.put(self.endpoint + '1/',
                                   data=json.dumps(question),
                                   content_type='application/json',
                                   headers=self.auth_headers)

        self.assertEqual(response.status_code, 200)
        results = self.client.get(self.endpoint + '1/', headers=self.auth_headers)

        content = json.loads(results.get_data(as_text=True))
        self.assertEqual(content['title'], question['title'])

    def test_question_can_be_posted(self):

        """
            Initial user registration and login
        """

        question = {
            "title": "How is reactJS",
            "body": "Just run the docs, you'll see"
        }
        response = self.client.post(self.endpoint,
                                    data=json.dumps(question),
                                    content_type='application/json',
                                    headers=self.auth_headers)

        """ asset if status is 201 for created """
        self.assertEqual(response.status_code, 201)
        results = self.client.get(self.endpoint + '2/', headers=self.auth_headers)

        content = json.loads(results.get_data(as_text=True))
        self.assertEqual(content['title'], question['title'])


if __name__ == '__main__':
    unittest.main()
