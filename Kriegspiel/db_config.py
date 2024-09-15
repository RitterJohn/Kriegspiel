import psycopg2

PGUSER = "USERNAME"
PGPASSWORD = "PASSWORD"
ip = "IP"
DATABASE = "DATABASE_NAME"

conn = psycopg2.connect(host=ip, database = DATABASE, user = PGUSER, password=PGPASSWORD)