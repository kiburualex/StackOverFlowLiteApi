import unittest
import json

from .base import BaseTestCase


class AnswerTestCase(BaseTestCase):

    endpoint = 'api/v1/questions/'

    def test_post_answer(self):
        """Test API can create a question (POST request)"""

        """ create a question first """
        question = {
            'id': 1,
            'title': 'Build an API',
            'description': 'How does one build an api',
            'answers': []
        }
        response = self.client.post(self.endpoint,
                                    data=json.dumps(question),
                                    content_type='application/json')

        """ assert if status code is 201 """
        self.assertEqual(response.status_code, 201)

        """ assert response is of json type """
        self.assertEqual(response.content_type, 'application/json')

        """ convert the response to text and retrieve the id """
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

    def test_api_can_get_answers_of_a_question_by_question_id(self):
        """ Test API can get answers of question by question id."""
        response = self.client.get(self.endpoint + '1/')
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.get_data(as_text=True))
        answers = content['answers']

        """ assert if answers response is a list """
        self.assertIsInstance(answers, list)


if __name__ == '__main__':
    unittest.main()
