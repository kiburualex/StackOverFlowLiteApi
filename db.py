import sys
import subprocess
import psycopg2, psycopg2.extras
from passlib.hash import sha256_crypt

dbname = 'saleor'
con = None
project_dir_name = "app"


class Database:
    def __init__(self):
        self.con = None
        self.dbhost = '127.0.0.1'
        self.dbname = 'saleor'
        self.dbuser = 'saleor'
        self.dbpassword = 'saleor'
        self.project_dir_name = 'app'

    def connect_postgres(self):
        self.con = psycopg2.connect(dbname='postgres', user='postgres', host='127.0.0.1', password='root')
        self.con.autocommit = True
        return self.con

    def connect_database(self):
        con_statement = "dbname='" + str(self.dbname) + "' user='" + str(self.dbuser) + "' host='" + str(
            self.dbhost) + "' password='" + str(self.dbpassword) + "'"
        self.con = psycopg2.connect(con_statement)
        self.con.autocommit = True
        return self.con

    def close_connection(self):
        self.con.close()

    def create_resources(self):
        try:
            con = self.connect_postgres()
            cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("select * from pg_database where datname = %(dname)s", {'dname': dbname})
            answer = cur.fetchall()
            if len(answer) > 0:
                print "Database {} exists".format(dbname)
                cur.execute("DROP DATABASE saleor")
                cur.execute("DROP ROLE saleor")
                self.create_database_resources(cur, con)
            else:
                print "Database {} does NOT exist".format(dbname)
                self.create_database_resources(cur, con)
        except Exception, e:
            print "Error %s" % e
            sys.exit(1)
        finally:
            if con:
                con.close()

    def create_database_resources(self, cur, con):
        try:
            cur.execute("CREATE ROLE saleor WITH SUPERUSER CREATEDB CREATEROLE LOGIN PASSWORD 'saleor'")
            cur.execute('CREATE DATABASE {} OWNER saleor;'.format('saleor'))
            con.close()
            conn = self.connect_database()
            cur2 = conn.cursor()
            cur2.execute('CREATE EXTENSION {};'.format('hstore'))
            cur2.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
            conn.commit()
            conn.close()
            self.generate_license_and_migrate()
        except Exception, e:
            print (e)

    def generate_license_and_migrate(self):
        try:
            keyfiles = self.generate_license()
            keyfile, check = keyfiles.split('###')
            keyfile = keyfile.replace('\r', '').replace('\n', '')
            check = check.replace('\r', '').replace('\n', '')

            subprocess.call(['python', '..\\' + project_dir_name + '\manage.pyc', 'makemigrations'], shell=True)
            subprocess.call(['python', '..\\' + project_dir_name + '\manage.pyc', 'migrate', ], shell=True)
            conn2 = self.connect_database()
            cur3 = conn2.cursor()
            cur3.execute(
                """INSERT INTO userprofile_user(name, email, is_superuser, is_active, is_staff, password, image, send_mail, date_joined) values('admin', 'admin@example.com', True, True, True, 'pbkdf2_sha256$30000$28uVy3qLTKlJ$npN/SiLkufzhREcOyYQFmWmzh1s/ZIo5qXk9/qSWSmE=','', True, now())""")
            cur3.execute(
                """INSERT INTO site_files(file, "check", created, modified) values('""" + keyfile + """', '""" + check + """', now(), now())""")
            conn2.commit()
            conn2.close()
        except Exception, e:
            print (e)


        def connect_to_stackoverflow_database(self):
            pass

        def create_user_table(self):
            try:
                con.close()
                conn = self.connect_database()
                cur = conn.cursor()
                cur.execute("DROP TABLE IF EXISTS users")
                cur.execute("CREATE TABLE users(id serial PRIMARY KEY, username varchar, \
                    email varchar,role varchar, password varchar);")
                # create ADmin user
                password = sha256_crypt.encrypt("pass123")
                cur.execute("INSERT INTO users( username, email, role, password) VALUES (%s, %s, %s, %s)", \
                            ("dess", "root@gmail.com", "Admin", password))
                cur.execute("SELECT * FROM users")
                items = cur.fetchall()
                print(items)
                print("Table Users Successfullyn Created")
                conn.commit()
            except Exception as e:
                print(e)



