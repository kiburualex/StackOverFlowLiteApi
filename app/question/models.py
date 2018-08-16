class Question():
    def __init__(self, api):
        self.api = api
        self.counter = 0
        self.questions = [
            {
                'id': 1,
                'title': 'Build an API',
                'description': 'How does one build an api',
                'answers': [
                    {
                        'id': 1,
                        'answer': 'Sample Answer',
                        'user': 'Leah'
                    },
                    {
                        'id': 2,
                        'answer': 'Sample Answer 2',
                        'user': 'Kim'
                    }
                ]
            },
            {
                'id': 2,
                'title': 'Learn React',
                'description': 'Read the documents',
                'answers': [
                    {
                        'id': 3,
                        'answer': 'Sample Answer',
                        'user': 'Paul'
                    },
                ]
            }
        ]

    def get(self, id):
        for question in self.questions:
            if question['id'] == id:
                return question
        self.api.abort(404, "Question {} doesn't exist".format(id))

    def create(self, data):
        question = data
        question['id'] = self.counter = self.counter + 1
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
