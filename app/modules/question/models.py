import psycopg2
import psycopg2.extensions
from psycopg2.extras import RealDictCursor
from config import BaseConfig
from app.utils.utils import db_config
from app.api.v1 import api


class Question:
    def __init__(self, data={}):

        """ Dynamic Databse URI config """

        self.config = db_config(BaseConfig.DATABASE_URI)
        self.table = 'questions'
        self.title = data.get('title')
        self.body = data.get('body')
        self.q = data.get('q')
        self.question_id = data.get('id')
        self.user_id = data.get('user_id')

    def save(self):

        """ Create a question record in questions table
        :return: None or record values
        """

        if not self.title or not self.body:
            api.abort(400, "Incorrect Data Format. Try again")

        """ check if question exists """

        question_exists = self.filter_by_title()

        if question_exists:
            api.abort(409, "Question with that title already exists.")

        con = psycopg2.connect(**self.config)
        cur, response = con.cursor(cursor_factory=RealDictCursor), None

        try:

            query = "INSERT INTO questions (title, body, user_id) VALUES (%s, %s, %s) RETURNING *"
            cur.execute(query, (self.title, self.body, self.user_id))
            con.commit()
            response = cur.fetchone()

        except Exception as e:
            print(e)

        con.close()
        return response

    def fetch_all(self):

        """
            Query the data in question table :return: list: query set list
        """

        con, queryset_list = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)

        try:

            cur.execute("SELECT * FROM questions")
            queryset_list = cur.fetchall()

        except Exception as e:
            print(e)

        con.close()
        return queryset_list

    def filter_by_title(self):

        """ Fetch User By Email """

        """ validate data """
        if not self.title or not self.body:
            api.abort(400, "Incorrect Data Format. Try again")

        con, results = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute("select * from {} WHERE title='{}'".format(self.table, self.title))
            results = cur.fetchone()
        except Exception as e:
            print(e)

        con.close()
        return results

    def update(self):

        """
            Update a question
            :return: bool:
        """

        """ validate data """
        if not self.title or not self.body:
            api.abort(400, "Incorrect Data Format. Try again")

        con, result = psycopg2.connect(**self.config), True
        cur = con.cursor(cursor_factory=RealDictCursor)

        try:

            query = "UPDATE questions SET title=%s, body=%s WHERE id=%s"
            cur.execute(query, (self.title, self.body, self.question_id))
            con.commit()
            con.close()

            return self.get_by_id()

        except Exception as e:
            print(e)

        api.abort(404, "Question {} doesn't exist".format(self.question_id))

    def delete(self):

        """ Delete a question """

        """ Check if questions exists """

        self.get_by_id()

        con = psycopg2.connect(**self.config)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:

            query = "DELETE FROM questions WHERE id=%s"
            cur.execute(query, [self.question_id])
            con.commit()
            con.close()
            return {"status": "success", "message": "question deleted successfully"}, 202

        except Exception as e:
            print(e)
        con.close()
        return {"status": "fail", "message": "failed to delete question"}, 400

    def get_by_id(self):

        """ Get a question by Id """

        con, response = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)

        try:

            query = "SELECT * FROM questions WHERE id = %s;"
            cur.execute(query, [self.question_id])
            con.commit()
            response = cur.fetchone()

            if response:
                return response

        except Exception as e:
            print(e)

        con.close()
        api.abort(404, "Question {} doesn't exist".format(self.question_id))