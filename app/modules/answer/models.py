import psycopg2
import psycopg2.extensions
from psycopg2.extras import RealDictCursor
from config import BaseConfig
from app.utils import db_config
from app.api.v1 import api
from app.modules.question.models import Question


class Answer:
    def __init__(self, data={}):
        self.config = db_config(BaseConfig.DATABASE_URI)
        self.table = 'answers'
        self.answer_body = data.get('answer_body')
        self.question_id = data.get('question_id')
        self.answer_id = data.get('answer_id')
        self.accepted = data.get('accepted')
        self.user_id = data.get('user_id')

    def save(self):
        """
        Creates an answer record in answers table
        :return: None of inserted record
        """
        con, response = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)

        if self.answer_body.strip() and type(self.user_id) == int and type(self.question_id) == int:
            try:
                query = "INSERT INTO answers (user_id, answer_body, question_id) VALUES (%s, %s, %s) RETURNING *; "
                cur.execute(query, (self.user_id, self.answer_body, self.question_id))
                con.commit()
                response = cur.fetchone()
            except Exception as e:
                print(e)
            con.close()
            return response
        api.abort(400, "Incorrect Input Data".format(self.answer_id))

    def fetch_all(self):
        """
        Fetch all records from a answers table
        :return: list: query set
        """
        Question({"id": self.question_id}).get_by_id()
        con = psycopg2.connect(**self.config)
        cur = con.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * FROM answers WHERE question_id=%s"
        cur.execute(query, [self.question_id])
        queryset_list = cur.fetchall()
        con.close()
        return queryset_list

    def question_author(self):
        con = psycopg2.connect(**self.config)
        try:
            cur = con.cursor(cursor_factory=RealDictCursor)
            query = "SELECT user_id FROM questions WHERE id=%s"
            cur.execute(query, self.question_id)
            return cur.fetchall()

        except Exception as e:
            print(e)
        con.close()
        return False

    def answer_author(self):
        try:
            con = psycopg2.connect(**self.config)
            cur = con.cursor(cursor_factory=RealDictCursor)
            query = "SELECT user_id FROM answers WHERE id=%s"
            cur.execute(query, self.answer_id)
            queryset_list = cur.fetchall()
            con.close()
            return queryset_list
        except Exception as e:
            return False

    def update_answer(self):
        con, result = psycopg2.connect(**self.config), True
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            query = "UPDATE answers SET answer_body=%s WHERE id=%s"
            cur.execute(query, (self.answer_body, self.answer_id))
            con.commit()
            con.close()
            return self.get_by_id()
        except Exception as e:
            print(e)

        api.abort(404, "Answer {} doesn't exist".format(self.answer_id))

    def accept(self, id):
        con, result = psycopg2.connect(**self.config), True
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            query = "UPDATE answers SET accepted=%s WHERE id=%s AND question_id=%s"
            cur.execute(query, (True, self.answer_id, self.question_id))
            con.commit()
            con.close()
            return self.get_by_id()
        except Exception as e:
            print(e)

        api.abort(404, "Answer {} doesn't exist".format(self.answer_id))

    def deny(self, id):
        con, result = psycopg2.connect(**self.config), True
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            query = "UPDATE answers SET accepted=%s WHERE id=%s AND question_id=%s"
            cur.execute(query, (False, self.answer_id, self.question_id))
            con.commit()
            con.close()
            return self.get_by_id()
        except Exception as e:
            print(e)

        api.abort(404, "Answer {} doesn't exist".format(self.answer_id))

    def delete(self):
        self.get_by_id()  # check user exists first
        con = psycopg2.connect(**self.config)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            query = "DELETE FROM answers WHERE id=%s"
            cur.execute(query, [self.answer_id])
            con.commit()
            con.close()
        except Exception as e:
            print(e)
            con.close()
            return False
        return True

    def get_by_id(self):
        con, response = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            query = "SELECT * FROM answers WHERE id = %s;"
            cur.execute(query, [self.answer_id])
            con.commit()
            response = cur.fetchone()
            if response:
                return response
            self.api.abort(404, "Answer {} doesn't exist".format(self.answer_id))
            con.close()
        except Exception as e:
            print(e)
        api.abort(404, "Answer {} doesn't exist".format(self.answer_id))
