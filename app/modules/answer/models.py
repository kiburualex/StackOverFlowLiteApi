import psycopg2
import psycopg2.extensions
from psycopg2.extras import RealDictCursor
from datetime import datetime
from config import BaseConfig
from app.utils.utils import db_config
from app.api.v1 import api
from app.modules.question.models import Question
from app.modules.user.models import User
from flask import request
from app.utils.auth_helper import Auth


class Answer:
    def __init__(self, data={}):

        """ Dynamic Databse URI config """

        self.config = db_config(BaseConfig.DATABASE_URI)
        self.table = 'answers'
        self.answer_body = data.get('answer_body')
        self.question_id = data.get('question_id')
        self.answer_id = data.get('answer_id')
        self.accepted = data.get('accepted')
        self.user_id = data.get('user_id')
        self.now = str(datetime.now())
        self.logged_in_user_id = Auth.get_logged_in_user(request)[0]['data']['user_id']

    def save(self):

        """
            Creates an answer record in answers table
            :return: None of inserted record
        """

        con, response = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)

        if not self.answer_body or not str(self.question_id).isdigit() or \
                not str(self.logged_in_user_id).isdigit():
            api.abort(400, "Incorrect Data Format. Try again")

        """ check if questions exists """
        Question({"id": self.question_id}).get_by_id()

        """ check if user exists """
        User({"id": self.logged_in_user_id}).get_by_id()

        answer_exists = self.filter_by_body()

        if answer_exists:
            api.abort(409, "Answer with that title already exists.")

        if self.answer_body.strip() and type(self.logged_in_user_id) == int and type(self.question_id) == int:
            try:
                query = "INSERT INTO answers (user_id, answer_body, question_id, created_at) \
                        VALUES (%s, %s, %s, %s) RETURNING *; "
                cur.execute(query, (self.logged_in_user_id, self.answer_body, self.question_id, self.now))
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

        """ check first if question exists """
        Question({"id": self.question_id}).get_by_id()

        con = psycopg2.connect(**self.config)
        cur = con.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * FROM answers WHERE question_id=%s"
        cur.execute(query, [self.question_id])

        queryset_list = cur.fetchall()
        con.close()

        return queryset_list

    def filter_by_body(self):

        """ Fetch User By Email """

        """ validate data """
        if not self.answer_body:
            api.abort(400, "Incorrect Data Format. Try again")

        con, results = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute("select * from {} WHERE answer_body='{}'".format(self.table, self.answer_body))
            results = cur.fetchone()
        except Exception as e:
            print(e)

        con.close()
        return results

    def update(self):

        """ Update an Answer """

        """ validate the answer details """

        if not self.answer_body:
            api.abort(400, "Incorrect Data Format. Try again")

        if type(self.accepted) != bool:
            api.abort(400, "Not a boolean (e.g True or False). Try again")

        con, result = psycopg2.connect(**self.config), True
        cur = con.cursor(cursor_factory=RealDictCursor)

        try:

            query = "UPDATE answers SET answer_body=%s, accepted=%s WHERE id=%s"
            cur.execute(query, (self.answer_body, self.accepted, self.answer_id))
            con.commit()
            con.close()

            return self.get_by_id()

        except Exception as e:
            print(e)

        api.abort(404, "Answer {} doesn't exist".format(self.answer_id))

    def delete(self):
        """ Delete an answer """

        """ check if answer id exists """
        self.get_by_id()

        con = psycopg2.connect(**self.config)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:

            query = "DELETE FROM answers WHERE id=%s"
            cur.execute(query, [self.answer_id])
            con.commit()
            con.close()

            return {"status": "success", "message": "answer deleted successfully"}, 202
        except Exception as e:
            print(e)
        con.close()
        return {"status": "fail", "message": "failed to delete answer"}, 400

    def get_by_id(self):

        """ Get answer by Id """

        con, response = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)

        try:

            query = "SELECT * FROM answers WHERE id = %s;"
            cur.execute(query, [self.answer_id])
            con.commit()
            response = cur.fetchone()

            if response:
                return response

        except Exception as e:
            print(e)

        con.close()
        api.abort(404, "Answer {} doesn't exist".format(self.answer_id))
