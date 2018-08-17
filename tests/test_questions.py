import unittest
import json

from .base import BaseTestCase

class QuestionTestCase(BaseTestCase):

    endpoint = 'api/v1/questions/'

    def test_home_status_code(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)

    def test_api_can_get_all_list_users(self):
        """Test API can get all questions (GET request)."""
        response = self.client.get(self.endpoint)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_api_can_get_user_by_id(self):
        """Test API can get a single question by using it's id."""
        response = self.client.get(self.endpoint + '1/')
        self.assertEqual(response.status_code, 200)

    def test_user_can_be_edited(self):
        """Test API can edit an existing question. (PUT request)"""

        question = {
            "id": 1,
            "title": "Build an API",
            "description": "How does one build an api",
            "answers": []
        }
        response = self.client.put(self.endpoint + '1/',
                                    data=json.dumps(question),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        results = self.client.get(self.endpoint + '1/')

        content = json.loads(results.get_data(as_text=True))
        self.assertEqual(content, question)

    def test_post_answer(self):
        """Test API can create a question (POST request)"""
        question = {
            'id': 1,
            'title': 'Build an API',
            'description': 'How does one build an api',
            'answers': []
        }
        response = self.client.post(self.endpoint,
                                    data=json.dumps(question),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')

        content = json.loads(response.get_data(as_text=True))

        question_id = str(content['id'])

        """ Post answers """
        answer = {
            'id': 1,
            'answer': 'Sample Answer',
            'user': 'Leah'
        }
        answer_response = self.client.post(self.endpoint + question_id + '/answer',
                                           data=json.dumps(answer),
                                           content_type='application/json')
        self.assertEqual(answer_response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
