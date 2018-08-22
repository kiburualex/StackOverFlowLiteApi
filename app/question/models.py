from app.dbmanager import Database
from app.user.models import User


class Question:
    def __init__(self, api):
        self.api = api
        self.db = Database()
        self.users = User(api)

    def fetch_all(self):
        self.db.query("SELECT * FROM questions")
        questions_tuple = self.db.cur.fetchall()
        questions = []
        for question in questions_tuple:
            questions.append(self.question_serializer(question))
        return questions

    def create(self, data):
        question = dict()
        question['title'] = str(data.get('title'))
        question['description'] = str(data.get('description'))
        question['user_id'] = str(data.get('user_id'))

        """ checks if user id exists"""
        self.users.get_user_by_id(question['user_id'])

        if self.check_if_question_exists(question['title']) is False:
            self.db.query(
                """
                INSERT INTO questions (title, description, user_id)
                VALUES (%s , %s, %s) RETURNING id;
                """,
                (question['title'], question['description'], question['user_id']))
            question_id = self.db.cur.fetchone()[0]
            self.db.save()

            return self.get_question_by_id(question_id)
        self.api.abort(409, "Question ({}) already exists".format(question['title']))

    def update(self, id, data):
        self.db.query("UPDATE questions SET title = %s, description \
            = %s WHERE id \
            = %s;", (
            data.get('title'),
            data.get('description'), id)
        )
        question = self.get_question_by_id(id)
        self.db.save()
        return question

    def delete(self, id):
        """ check user exists first """
        user = self.get_question_by_id(id)
        self.db.query(
            "DELETE FROM questions WHERE id=%s", (id, ))
        self.db.save()
        return "Deleted Successfully"

    def check_if_question_exists(self, title):
        """ check if user with the same username already exist """
        self.db.query("SELECT * FROM questions WHERE title = %s;", (title,))
        question = self.db.cur.fetchone()
        self.db.save()
        if question:
            return self.question_serializer(question)
        else:
            return False

    def get_question_by_id(self, id):
        """ Serialize tuple into dictionary """
        self.db.query("SELECT * FROM questions WHERE id = %s;", (id,))
        question = self.db.cur.fetchone()
        if question:
            return self.question_serializer(question)
        self.api.abort(404, "Question {} doesn't exist".format(id))

    def question_serializer(self, question):
        """ Serialize tuple into dictionary """
        question_details = dict(
            id=question[0],
            title=question[1],
            description=question[2],
            user_id=question[3]
        )
        return question_details

