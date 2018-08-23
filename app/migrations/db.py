import psycopg2
import psycopg2.extras
import os
from .initial_data import migrations
from config import BaseConfig
from ..utils import db_config


class Database:
    def __init__(self, config):
        self.config = db_config(config)
        self.database = self.config.get('database')

    def migrate(self):
        con = psycopg2.connect(**self.config)
        con.autocommit = True
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("select * from pg_database where datname = %(database_name)s", {'database_name': self.database})
        databases = cur.fetchall()
        if len(databases) > 0:
            for command in migrations:
                try:
                    cur.execute(command)
                    con.commit()
                except Exception as e:
                    print(e)
        else:
            """ create the database and the user """
            cur.execute(
                "CREATE ROLE {} WITH SUPERUSER CREATEDB CREATEROLE LOGIN PASSWORD '{}';".format(self.config.get('user'),
                                                                                                self.config.get('user')))
            cur.execute('CREATE DATABASE {} OWNER {};'.format(self.database, self.config.get('user')))
            for command in migrations:
                try:
                    cur.execute(command)
                    con.commit()
                except Exception as e:
                    print(e)
        con.close()

    def migrate_test_db(self):
        """ Create test database and schema """
        os.environ['APP_SETTINGS'] = 'TESTING'
        con = psycopg2.connect(**self.config)
        con.autocommit = True
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print('\n* Creating test db\n')
        try:
            cur.execute('CREATE DATABASE {} OWNER {};'.format(BaseConfig.TEST_DB, self.config.get('user')))
        except Exception as e:
            print(e)
            pass
        con.close()
        self.config['database'] = BaseConfig.TEST_DB
        con = psycopg2.connect(**self.config)
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        for command in migrations:
            try:
                cur.execute(command)
                con.commit()
                pass
            except Exception as e:
                print(e)
        con.close()

    def create_default_user(self):
        from passlib.hash import sha256_crypt
        self.config = db_config(BaseConfig.DATABASE_URI)
        con = psycopg2.connect(**self.config)
        con.autocommit = True
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        password = sha256_crypt.encrypt("admin123")
        cur.execute("INSERT INTO users (username, email, role, password) VALUES (%s, %s, %s, %s)", \
                    ("admin", "admin@example.com", "admin", password))
        con.close()

    def drop_test_database(self):
        print('\n * Dropping test database \n')
        os.environ['APP_SETTINGS'] = 'DEVELOPMENT'
        self.config = db_config(BaseConfig.DATABASE_URI)
        con = psycopg2.connect(**self.config)
        con.autocommit = True
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('DROP DATABASE IF EXISTS {};'.format(BaseConfig.TEST_DB))
        con.close()
        os.environ['APP_SETTINGS'] = 'TESTING'


db = Database(BaseConfig.DATABASE_URI)
