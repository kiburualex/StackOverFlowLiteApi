import psycopg2
import os

dbname = os.getenv("DBNAME", "testdb")
dbuser = os.getenv("DBUSER", "postgres")
dbpass = os.getenv("PASSWORD", "root123")
dbhost = os.getenv("DBHOST", "localhost")
DATABASE_URL = os.getenv('DATABASE_URL', "postgres://umanzqjsaguhpj:\
d7bc453a7b72c1c258ee1fae3f8e476a9c4192a8cc532d86a386c41ec9b2dab7@\
ec2-23-23-226-190.compute-1.amazonaws.com:5432/d9ptd14ruqavrg")

try:
    conn = psycopg2.connect(DATABASE_URL)
except:
    print("I am unable to connect to the database")