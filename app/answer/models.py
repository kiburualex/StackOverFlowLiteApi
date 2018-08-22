from app.dbmanager import Database
from app.user.models import User
from app.question.models import Question


class Answer:
    def __init__(self, api):
        self.api = api
        self.db = Database()
        self.user = User(api)
        self.question = Question(api)

    def fetch_all(self, question_id):
        self.db.query("SELECT * FROM answers WHERE question_id = %s;", (question_id,))
        answers_tuple = self.db.cur.fetchall()
        answers = []
        for answer in answers_tuple:
            answers.append(self.answer_serializer(answer))
        return answers

    def create(self, question_id, data):
        answer = dict()
        answer['description'] = str(data.get('description'))
        answer['user_id'] = data.get('user_id')
        answer['question_id'] = question_id

        """ checks if question id exists"""
        self.question.get_question_by_id(question_id)

        """ checks if user id exists"""
        self.user.get_user_by_id(answer['user_id'])

        if self.check_if_answers_exists(answer['description']) is False:
            self.db.query(
                """
                INSERT INTO answers (description, user_id, question_id)
                VALUES (%s , %s, %s) RETURNING id;
                """,
                (answer['description'], answer['user_id'], question_id))
            answer_id = self.db.cur.fetchone()[0]
            self.db.save()

            return self.get_answer_by_id(answer_id)
        self.api.abort(409, "Answer already exists")

    def update(self, id, data):
        self.db.query("UPDATE answers SET description \
            = %s WHERE id \
            = %s;", (
            data.get('description'), id)
        )
        answer = self.get_answer_by_id(id)
        self.db.save()
        return answer

    def delete(self, id):
        """ check answers exists first """
        self.get_answer_by_id(id)
        self.db.query(
            "DELETE FROM answers WHERE id=%s", (id, ))
        self.db.save()
        return "Deleted Successfully"

    def check_if_answers_exists(self, description):
        """ check if user with the same username already exist """
        self.db.query("SELECT * FROM answers WHERE description = %s;", (description,))
        answer = self.db.cur.fetchone()
        self.db.save()
        if answer:
            return self.answer_serializer(answer)
        else:
            return False

    def get_answer_by_id(self, id):
        """ Serialize tuple into dictionary """
        self.db.query("SELECT * FROM answers WHERE id = %s;", (id,))
        answer = self.db.cur.fetchone()
        if answer:
            return self.answer_serializer(answer)
        self.api.abort(404, "Answer doesn't exist")

    def answer_serializer(self, answer):
        """ Serialize tuple into dictionary """
        answer_details = dict(
            id=answer[0],
            user_id=answer[1],
            question_id=answer[2],
            description=answer[3],
            accepted=answer[4]
        )
        return answer_details

    def accept(self, id):
        """ A method to accept answers """
        status = True
        self.db.query(
            "UPDATE answer SET status = %s WHERE id \
                = %s;", (status, id))
        self.db.save()
        return self.get_answer_by_id(id)

    def deny(self, id):
        """ A method to deny answers """
        status = False
        self.db.query(
            "UPDATE answers SET status = %s WHERE id \
                = %s;", (status, id))
        self.db.save()
        return self.get_answer_by_id(id)

