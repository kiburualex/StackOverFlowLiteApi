import sys
import psycopg2, psycopg2.extras
from passlib.hash import sha256_crypt


class DatabaseSetup:
    def __init__(self):
        self.con = None
        self.dbhost = '127.0.0.1'
        self.dbname = 'stack'
        self.db_testing = 'stack_testing'
        self.dbuser = 'stack'
        self.dbpassword = 'stack'

    def connect_to_stack_database(self):
        """ connect to the StackOverFlow-lite database called stack """
        try:
            self.con = psycopg2.connect(dbname=self.dbname, user=self.dbuser, host=self.dbhost, password=self.dbpassword)
            self.con.autocommit = True
            return self.con
        except BaseException as e:
            print(e)

    def create_users_table(self):
        """ create users table """
        try:
            con = self.connect_to_stack_database()
            cur = con.cursor()
            cur.execute('CREATE EXTENSION {};'.format('hstore'))
            cur.execute("CREATE TABLE users ("
                        "id serial PRIMARY KEY, "
                        "username varchar, "
                        "email varchar, "
                        "role varchar, "
                        "password varchar);"
                        )
            password = sha256_crypt.encrypt("admin123")
            cur.execute("INSERT INTO users (username, email, role, password) VALUES (%s, %s, %s, %s)",
                        ("admin", "admin@example.com", "admin", password))
            cur.execute("SELECT * FROM users")
            items = cur.fetchall()
            print(items)
            con.commit()
            con.close()
        except Exception as e:
            print (e)

    def create_questions_table(self):
        """ create questions table """
        try:
            con = self.connect_to_stack_database()
            cur = con.cursor()
            cur.execute("CREATE TABLE questions ("
                        "id serial PRIMARY KEY, "
                        "title varchar, "
                        "description varchar, "
                        "user_id INTEGER, "
                        "date_created TIMESTAMP, "
                        "FOREIGN KEY (user_id) REFERENCES users (id));"
                        )
            con.commit()
            con.close()
        except Exception as e:
            print (e)

    def create_answers_table(self):
        """ create answers table """
        try:
            con = self.connect_to_stack_database()
            cur = con.cursor()
            cur.execute("CREATE TABLE answers ("
                        "id serial PRIMARY KEY, "
                        "user_id INTEGER, "
                        "question_id INTEGER, "
                        "description varchar, "
                        "accepted BOOLEAN DEFAULT FALSE, "
                        "date_created TIMESTAMP, "
                        "FOREIGN KEY (user_id) REFERENCES users (id), "
                        "FOREIGN KEY (question_id) REFERENCES questions (id));"
                        )
            con.commit()
            con.close()
        except Exception as e:
            print (e)

    def process_configuration(self):
        try:
            """ 
                connect to default postgres 
            """
            self.con = psycopg2.connect(dbname='postgres', user='postgres', host='127.0.0.1', password='root')
            self.con.autocommit = True
            cur = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("select * from pg_database where datname = %(dname)s", {'dname': self.dbname})
            results = cur.fetchall()
            if len(results) > 0:
                """ check if stack database exists """
                cur.execute("DROP DATABASE {};".format(self.dbname))
                cur.execute("DROP ROLE {};".format(self.dbuser))
            cur.execute(
                "CREATE ROLE {} WITH SUPERUSER CREATEDB CREATEROLE LOGIN PASSWORD '{}';".format(self.dbuser, self.dbuser))
            cur.execute('CREATE DATABASE {} OWNER {};'.format(self.dbname, self.dbname))

            self.con.close()

            self.create_users_table()
            self.create_questions_table()
            self.create_answers_table()

        except Exception as e:
            print(e)
            sys.exit(1)


db = DatabaseSetup()
db.process_configuration()


