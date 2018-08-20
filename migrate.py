import psycopg2
import os
from passlib.hash import sha256_crypt
from connect import conn


def create_users():
    """ Function To create users table"""

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


def create_requests():
    """ Function To create requests table"""

    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS requests")
    cur.execute("CREATE TABLE requests(id serial PRIMARY KEY, user_id integer, \
    category varchar, location varchar, req_date date, description varchar, \
    status varchar, isresolved boolean);")
    print("Table requests Successfullyn Created")
    conn.commit()


def create_blacklist_tokens():
    """ Function To create blacklist_tokens table"""

    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS blacklist_tokens")
    cur.execute("CREATE TABLE blacklist_tokens(id serial PRIMARY KEY, token varchar,\
        blacklisted_on date);")
    conn.commit()
    print("Table blacklist_tokens Successfullyn Created")


create_users()
create_requests()
create_blacklist_tokens()