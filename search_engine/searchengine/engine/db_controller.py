from searchengine import app
from flask_mysqldb import MySQL

class DBController:
    def __init__(self):
        self.__mysql = MySQL()
        self.__mysql.init_app(app)

    def add_user(self, uname):
        fetch_sql = "SELECT * FROM users WHERE u_name = '{}'".format(uname)
        cur = self.__mysql.connection.cursor()
        cur.execute(fetch_sql)
        data = cur.fetchall()
        if len(data) == 0:
            insert_sql = "INSERT INTO users VALUES (DEFAULT, '{}')".format(uname)
            cur.execute(insert_sql)
            self.__mysql.connection.commit()

