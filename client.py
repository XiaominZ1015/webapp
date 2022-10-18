import psycopg2

con = psycopg2.connect(
            host="localhost",
            database="users_db",
            user="webapp",
            password="zxm123456")

cur = con.cursor()
