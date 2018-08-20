import sys
import psycopg2, psycopg2.extras
from passlib.hash import sha256_crypt


class Database:
    def __init__(self):
        self.con = None
        self.dbhost = '127.0.0.1'
        self.dbname = 'stack'
        self.dbuser = 'stack'
        self.dbpassword = 'stack'

    def connect_to_stack_database(self):
        con_statement = "dbname='" + str(self.dbname) + "' user='" + str(self.dbuser) + "' host='" + str(
            self.dbhost) + "' password='" + str(self.dbpassword) + "'"
        self.con = psycopg2.connect(con_statement)
        self.con.autocommit = True
        return self.con

    def create_users_table(self):
        try:
            con = self.connect_to_stack_database()
            cur = con.cursor()
            cur.execute('CREATE EXTENSION {};'.format('hstore'))
            cur.execute("CREATE TABLE users ("
                        "id serial PRIMARY KEY, "
                        "name varchar, "
                        "email varchar, "
                        "password varchar);"
                        )
            password = sha256_crypt.encrypt("admin123")
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                        ("admin", "admin@example.com", password))
            cur.execute("SELECT * FROM users")
            items = cur.fetchall()
            print(items)
            print("Table Answers Successfully Created")
            con.commit()
            con.close()
        except Exception as e:
            print ("inside the create_user_table")
            print (e)

    def create_questions_table(self):
        try:
            con = self.connect_to_stack_database()
            cur = con.cursor()
            cur.execute("CREATE TABLE questions ("
                        "id serial PRIMARY KEY, "
                        "title varchar, "
                        "description varchar);"
                        )
            items = cur.fetchall()
            print(items)
            print("Table Questions Successfully Created")
            con.commit()
            con.close()
        except Exception as e:
            print ("inside the create_question_table")
            print (e)

    def create_answers_table(self):
        try:
            con = self.connect_to_stack_database()
            cur = con.cursor()
            cur.execute("CREATE TABLE answers (\
                        id serial PRIMARY KEY, \
                        title varchar, \
                        description varchar;"
                        )
            items = cur.fetchall()
            print(items)
            print("Table Answers Successfully Created")
            con.commit()
            con.close()
        except Exception as e:
            print ("inside the create_question_table")
            print (e)

    def process_configuration(self):
        try:
            """ connect to default postgres """
            self.con = psycopg2.connect(dbname='postgres', user='postgres', host='127.0.0.1', password='root')
            self.con.autocommit = True
            cur = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("select * from pg_database where datname = %(dname)s", {'dname': self.dbname})
            answer = cur.fetchall()
            if len(answer) > 0:
                """ check if stack database exists """
                cur.execute("DROP DATABASE {};".format(self.dbname))
                cur.execute("DROP ROLE {};".format(self.dbuser))
            cur.execute(
                "CREATE ROLE {} WITH SUPERUSER CREATEDB CREATEROLE LOGIN PASSWORD '{}';".format(self.dbuser, self.dbuser))
            cur.execute('CREATE DATABASE {} OWNER {};'.format(self.dbname, self.dbname))
            self.con.close()

            self.create_users_table()
            # self.create_answers_table()
            self.create_questions_table()

        except Exception as e:
            print ("inside the process_configuration")
            print(e)
            sys.exit(1)


db = Database()
db.process_configuration()


