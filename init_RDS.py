import sys

import mysql.connector


def initializeDB(name: str):
    db = mysql.connector.connect(host=sys.argv[1], user="csye6225", password="password")
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE users_db")
    #cursor.execute("SHOW DATABASES")
    cursor.execute("CREATE USER 'apiuser'@'%' IDENTIFIED BY '123456'")
    cursor.execute("GRANT ALL PRIVILEGES ON users_db.*  TO 'apiuser'@'%'")

if __name__ == "__main__":
    initializeDB(sys.argv[1:])
