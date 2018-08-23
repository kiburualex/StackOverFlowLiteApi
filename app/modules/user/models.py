import psycopg2
import psycopg2.extras
from psycopg2.extras import RealDictCursor
from flask_bcrypt import Bcrypt
from config import BaseConfig
from app.utils import db_config
from app.api.v1 import api


class User:
    def __init__(self, data={}):
        self.config = db_config(BaseConfig.DATABASE_URI)
        self.table, self.email = 'users', data.get('email')
        self.username, self.role = data.get('username'), data.get('role')
        self.user_id = data.get('id')
        self.b_crypt = Bcrypt()
        if data.get('password'):
            self.password = self.b_crypt.generate_password_hash(data.get('password')).decode('utf-8')

    def fetch_all(self):
        con = psycopg2.connect(**self.config)
        cur = con.cursor(cursor_factory=RealDictCursor)
        cur.execute("select * from {}".format(self.table))
        queryset_list = cur.fetchall()
        con.close()
        return [item for item in queryset_list]

    def filter_by_email(self):
        con, queryset_list = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("select * from {} WHERE email='{}'".format(self.table, self.email))
            queryset_list = cur.fetchall()
        except Exception as e:
            print(e)
        con.close()
        return queryset_list

    def update(self):
        """
        Update an user column
        :return: bool:
        """
        con, result = psycopg2.connect(**self.config), True
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            query = "UPDATE users SET email=%s, username=%s, role=%s WHERE id=%s"
            cur.execute(query, (self.email, self.username, self.role, self.user_id))
            con.commit()
            con.close()
            return self.get_by_id()
        except Exception as e:
            print(e)
        api.abort(404, "User {} doesn't exist".format(self.user_id))

    def delete(self):
        self.get_by_id() #check user exists first
        con = psycopg2.connect(**self.config)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            query = "DELETE FROM users WHERE id=%s"
            cur.execute(query, [self.user_id])
            con.commit()
            con.close()
        except Exception as e:
            print(e)
            con.close()
            return False
        return True

    def save(self):
        con, response = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            query = "INSERT INTO users (username, email, role, password) values(%s, %s, %s, %s) RETURNING *"
            cur.execute(query, (self.username, self.email, self.role, self.password))
            con.commit()
            response = cur.fetchone()
        except Exception as e:
            print(e)
        con.close()
        return response

    def get_by_id(self):
        con, response = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            query = "SELECT * FROM users WHERE id = %s;"
            cur.execute(query, [self.user_id])
            con.commit()
            response = cur.fetchone()
            if response:
                return response
            self.api.abort(404, "User {} doesn't exist".format(self.user_id))
            con.close()
        except Exception as e:
            api.abort(404, "User {} doesn't exist".format(self.user_id))

    def password(self, password):
        return self.b_crypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return self.b_crypt.check_password_hash(self.password_hash, password)
