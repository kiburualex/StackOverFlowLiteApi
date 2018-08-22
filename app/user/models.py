from passlib.hash import sha256_crypt
from app.dbmanager import Database


class User:
    def __init__(self, api):
        self.api = api
        self.db = Database()

    def fetch_all(self):
        self.db.query("SELECT * FROM users")
        users_tuple = self.db.cur.fetchall()
        users = []
        for user in users_tuple:
            users.append(self.user_serializer(user))
        return users

    def create(self, data):
        user = dict()
        user['username'] = str(data.get('username'))
        user['email'] = str(data.get('email'))
        user['role'] = str(data.get('role'))
        user['password'] = str(data.get('password'))

        if self.check_if_username_exists(user['username']) is False:
            hash_pass = sha256_crypt.encrypt(user['password'])
            self.db.query(
                """
                INSERT INTO users (username, email, role, password)
                VALUES (%s , %s, %s, %s) RETURNING id;
                """,
                (user['username'], user['email'], user['role'], hash_pass))
            user_id = self.db.cur.fetchone()[0]
            self.db.save()

            return self.get_user_by_id(user_id)
        self.api.abort(409, "User {} already exists".format(user['username']))

    def update(self, id, data):
        self.db.query("UPDATE users SET username = %s, email \
            = %s, role = %s WHERE id \
            = %s;", (
            data.get('username'),
            data.get('email'),
            data.get('role'), id)
        )
        user = self.get_user_by_id(id)
        self.db.save()
        return user

    def delete(self, id):
        """ check user exists first """
        self.get_user_by_id(id)
        self.db.query(
            "DELETE FROM users WHERE id=%s", (id, ))
        self.db.save()
        return "Deleted Successfully"

    def check_if_username_exists(self, username):
        """ check if user with the same username already exist """
        self.db.query("SELECT * FROM users WHERE username = %s;", (username,))
        user = self.db.cur.fetchone()
        self.db.save()
        if user:
            return self.user_serializer(user)
        else:
            return False

    def get_user_by_id(self, id):
        """ Serialize tuple into dictionary """
        self.db.query("SELECT * FROM users WHERE id = %s;", (id,))
        user = self.db.cur.fetchone()
        if user:
            return self.user_serializer(user)
        self.api.abort(404, "User {} doesn't exist".format(id))

    def user_serializer(self, user):
        """ Serialize tuple into dictionary """
        user_details = dict(
            id=user[0],
            username=user[1],
            email=user[2],
            role=user[3],
            password=user[4]
        )
        return user_details

    def verify_password(self, password, hashed_pass):
        """ Verify Password"""
        h_pass = sha256_crypt.verify(password, hashed_pass)
        return h_pass

    def change_role(self, username, role):
        self.db.query("UPDATE users SET role = %s\
         WHERE username = %s;", (role, username)
        )
        item = self.check_if_username_exists(username)
        self.db.save()
        return item
