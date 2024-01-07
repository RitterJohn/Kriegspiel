import psycopg2

PGUSER = "postgres"
PGPASSWORD = "123"
ip = "localhost"
DATABASE = "kriegspiel"

conn = psycopg2.connect(host=ip, database = DATABASE, user = PGUSER, password=PGPASSWORD)