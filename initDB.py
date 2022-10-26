import mysql.connector


def initializeDB():
    file1 = open('/etc/mysql/debian.cnf', 'r')
    file1.readline()
    file1.readline()
    file1.readline()
    file1.readline()
    passwordLine = file1.readline()
    file1.close()
    pwd = passwordLine[-17:]
    pwd = pwd[0:(len(pwd)-1)]
    db = mysql.connector.connect(host="localhost", user="debian-sys-maint", password=pwd)
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE users_db")
    #cursor.execute("SHOW DATABASES")
    cursor.execute("CREATE USER 'apiuser'@'localhost' IDENTIFIED BY '123456'")
    cursor.execute("GRANT ALL PRIVILEGES ON users_db.*  TO 'apiuser'@'localhost'")


initializeDB()
