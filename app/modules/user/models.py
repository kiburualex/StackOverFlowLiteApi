import datetime
import jwt
import psycopg2
import psycopg2.extras
from psycopg2.extras import RealDictCursor
from flask_bcrypt import Bcrypt
from config import BaseConfig
from app.utils.utils import db_config
from app.api.v1 import api
from config import key
from app.utils.utils import valid_email


class User:
    def __init__(self, data={}):

        """ Dynamic Databse URI config """

        self.config = db_config(BaseConfig.DATABASE_URI)

        self.b_crypt = Bcrypt()
        self.email = data.get('email')
        self.user_id = data.get('id')
        self.username = data.get('username')
        self.role = data.get('role')
        self.table = 'users'
        self.now = str(datetime.datetime.now())

        """ encrypt the password if provided """
        if data.get('password'):
            self.password = self.b_crypt.\
                generate_password_hash(data.get('password')).\
                decode('utf-8')

    def fetch_all(self):

        """ Get All Users """

        con = psycopg2.connect(**self.config)
        cur = con.cursor(cursor_factory=RealDictCursor)
        cur.execute("select * from {}".format(self.table))

        results = cur.fetchall()
        con.close()
        return [item for item in results]

    def filter_by_email(self):

        """ Fetch User By Email """

        """ validate email """
        if not valid_email(self.email):
            api.abort(400, "Incorrect Email ({}) Format. Try again".format(self.email))

        con, results = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute("select * from {} WHERE email='{}'".format(self.table, self.email))
            results = cur.fetchone()
        except Exception as e:
            print(e)

        con.close()
        return results

    def update(self):

        """ Update user """

        """ validate user details """

        if not valid_email(self.email):
            api.abort(400, "Incorrect Email ({}) Format. Try again".format(self.email))

        if not self.role or not self.username:
            api.abort(400, "Incorrect Data Format. Try again")

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

        """ Check user exists before deleting """

        self.get_by_id()
        con = psycopg2.connect(**self.config)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            query = "DELETE FROM users WHERE id=%s"
            cur.execute(query, [self.user_id])
            con.commit()
            con.close()

            return {"status": "success", "message": "user deleted successfully"}, 202
        except Exception as e:
            print(e)

        con.close()
        return {"status": "fail", "message": "failed to delete user"}, 400

    def save(self):

        """ Create a user """

        """ validate user details """

        if not valid_email(self.email):
            api.abort(400, "Incorrect Email ({}) Format. Try again".format(self.email))

        if not self.role or not self.username:
            api.abort(400, "Incorrect Data Format. Try again")

        user_exists = self.filter_by_email()

        if user_exists:
            api.abort(409, "That Email ({}) Already Exists".format(self.email))

        con, response = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)

        try:
            query = "INSERT INTO users (username, email, role, password, created_at) \
                     values(%s, %s, %s, %s, %s) RETURNING *"
            cur.execute(query, (self.username, self.email, self.role, self.password, self.now))
            con.commit()
            response = cur.fetchone()
        except Exception as e:
            print(e)

        con.close()
        return response

    def register_new_user(self):

        """
            Registering a new user assigns the user a token
            and allows them to login
        """
        new_user = self.save()
        if new_user:
            return self.generate_token(new_user)
        api.abort(400, "Incorrect Input format".format(self.user_id))

    def get_by_id(self):

        """ Get user by Id """
        con, response = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            query = "SELECT * FROM users WHERE id = %s;"
            cur.execute(query, [self.user_id])
            con.commit()
            response = cur.fetchone()

            if response:
                return response
        except Exception as e:
            print(e)

        con.close()
        api.abort(404, "User {} doesn't exist".format(self.user_id))

    def password(self, password):

        return self.b_crypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, email, password):

        self.email = email
        user = self.filter_by_email()
        password_hash = user.get('password')

        return self.b_crypt.check_password_hash(password_hash, password)

    def encode_auth_token(self, email):
        """
            Generates the Auth Token
            :return: string
        """
        try:
            self.email = email
            user = self.filter_by_email()
            user_id = user.get('id')
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(payload, key, algorithm='HS256')
        except Exception as e:
            return e

    def decode_auth_token(self, auth_token):
        """
            Decodes the auth token
            :param auth_token:
            :return: integer|string
        """
        try:

            payload = jwt.decode(auth_token, key, algorithms=['HS256'])
            is_blacklisted_token = Token().check_blacklist(auth_token)

            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']

        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'

        except jwt.InvalidTokenError as e:
            return 'Invalid token. Please log in again.'

    def generate_token(self, user):

        """ Generate token of the user """
        try:

            """ Encode Token using user details """

            auth_token = self.encode_auth_token(user.get('email'))

            response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
                'Authorization': auth_token.decode()
            }
            return response_object, 201

        except Exception as e:

            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return response_object, 401


class Token:
    def __init__(self, data={}):

        """ Dynamic Databse URI config """

        self.config = db_config(BaseConfig.DATABASE_URI)
        self.token = data.get('token')

    def save(self, token):

        """
            Saves Tokens in the Database
            :param token:
            :return: token
        """
        con, response = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)

        try:
            query = "INSERT INTO tokens (token) values (%s) RETURNING *"
            cur.execute(query, [token])
            con.commit()
        except Exception as e:
            print(e)
        con.close()

        return response

    def check_blacklist(self, token):
        """
            Checks To See If Token Exists
            :param token:
            :return: token
        """
        con, response = psycopg2.connect(**self.config), None
        cur = con.cursor(cursor_factory=RealDictCursor)

        try:
            query = "SELECT * FROM tokens WHERE token = %s;"
            cur.execute(query, [token])
            con.commit()
            response = cur.fetchone()
        except Exception as e:
            print(e)
        con.close()

        return response
