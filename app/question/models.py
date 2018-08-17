class Question():
    def __init__(self, api):
        self.api = api
        self.questions = [
            {
                "id": 1,
                "title": "Build an API",
                "description": "How does one build an api",
                "answers": [
                    {
                        "id": 1,
                        "answer": "Sample Answer",
                        "user": "Paul"
                    }
                ]
            }
        ]

    def get(self, question_id):
        for question in self.questions:
            if question['id'] == question_id:
                return question
        self.api.abort(404, "Question {} doesn't exist".format(question_id))

    def create(self, data):
        question = dict()
        question['title'] = str(data.get('title'))
        question['description'] = str(data.get('description'))
        question['answers'] = []

        """ Ensure table id column value is unique """
        try:
            question['id'] = int(self.questions[-1].get('id')) + 1
        except Exception as e:
            question['id'] = 1

        self.questions.append(question)

        return question

    def update(self, id, data):
        question = self.get(id)
        question.update(data)
        return question

    def delete(self, id):
        question = self.get(id)
        self.questions.remove(question)

    def get_answers(self, id):
        question = self.get(id)
        return question['answers']

    def create_answer(self, id, data):
        question = self.get(id)
        question['answers'].append(data)
        return data

    def delete_answer(self, question_id, answer_id):
        question = self.get(question_id)
        answer = list(filter(lambda d: d['id'] in [int(answer_id)], question['answers']))
        """ return a list and get the first element matching query """
        question['answers'].remove(answer[0])
