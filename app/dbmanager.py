import psycopg2, psycopg2.extras
from .querymanager import create_tables, drop_tables
from passlib.hash import sha256_crypt


class Database:
    def __init__(self, testing=None):
        self.con = None
        self.dbhost = '127.0.0.1'
        self.dbname = 'stack'
        self.dbuser = 'stack'
        self.dbpassword = 'stack'

        if testing:
            self.dbname = 'stack_testing'
            self.dbuser = 'stack_testing'
            self.dbpassword = 'stack_testing'
            self.create_test_database()

        self.con = psycopg2.connect(
            dbname=self.dbname,
            user=self.dbuser,
            host=self.dbhost,
            password=self.dbpassword)
        self.con.autocommit = True
        self.cur = self.con.cursor()

    def connect(self):
        pass

    def query(self, query, args=None):
        if args:
            self.cur.execute(query, args)
        else:
            self.cur.execute(query)

    def save(self):
        self.con.commit()

    def close(self):
        self.cur.close()
        self.con.close()

    def create_tables(self):
        for table in create_tables():
            self.query(table)
            self.save()

        return 'tables created'

    def drop_tables(self):
        ''' deletes the existing tables from the database'''
        for drop_table in drop_tables():
            self.query(drop_table)
            self.save()

    def create_initial_data(self):
        password = sha256_crypt.encrypt("admin123")
        self.query("INSERT INTO users (username, email, role, password) VALUES (%s, %s, %s, %s)",
                    ("admin", "admin@example.com", "admin", password))
        return 'data successfully added'

    def create_test_database(self):
        try:
            con = psycopg2.connect(dbname='postgres', user='postgres', host='127.0.0.1', password='root')
            con.autocommit = True
            cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("select * from pg_database where datname = %(dname)s", {'dname': self.dbname})
            results = cur.fetchall()
            if len(results) > 0:
                """ check if stack database exists """
                cur.execute("DROP DATABASE {};".format(self.dbname))
                cur.execute("DROP ROLE {};".format(self.dbuser))
            cur.execute(
            "CREATE ROLE {} WITH SUPERUSER CREATEDB CREATEROLE LOGIN PASSWORD '{}';".format(self.dbuser, self.dbuser))
            cur.execute('CREATE DATABASE {} OWNER {};'.format(self.dbname, self.dbname))

            con.close()

        except Exception as e:
            print(e)

