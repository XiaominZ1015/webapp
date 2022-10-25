import psycopg2
# to connect DB
con = psycopg2.connect(
            host="localhost",
            database="users_db",
            user="webapp",
            password="zxm123456")

cur = con.cursor()
