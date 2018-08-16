
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
                        'answer': 'Sample Answer',
                        'user': 'Leah'
                    },
                    {
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