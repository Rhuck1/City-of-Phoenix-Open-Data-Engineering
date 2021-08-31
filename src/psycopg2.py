import psycopg2

DB_HOST = 'postgres-on-aws-rds.coy8nrpagj4x.us-west-2.rds.amazonaws.com'
DB_NAME = 'postgres-on-aws-rds'
DB_USER = 'postgres'
DB_PASS = 'password'


conn = psycopg2.connect(dbname=DB_NAME,
                 user=DB_USER,
                 password=DB_PASS,
                 host=DB_HOST)




conn.close()