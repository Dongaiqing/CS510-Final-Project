from searchengine import app
from flask_mysqldb import MySQL

class DBController:
    def __init__(self):
        self.__mysql = MySQL()
        self.__mysql.init_app(app)

    def add_user(self, uname):
        fetch_sql = "SELECT * FROM users WHERE u_name = '{}'".format(uname)
        cursor = self.__mysql.connection.cursor()
        cursor.execute(fetch_sql)
        data = cursor.fetchall()
        if len(data) == 0:
            insert_sql = "INSERT INTO users VALUES (DEFAULT, '{}')".format(uname)
            cursor.execute(insert_sql)
            self.__mysql.connection.commit()
    
    def get_user_id(self, uname):
        fetch_sql = "SELECT * FROM users WHERE u_name = '{}'".format(uname)
        cursor = self.__mysql.connection.cursor()
        cursor.execute(fetch_sql)
        data = cursor.fetchone()
        return None if data is None else data[0]

    def record_user_click(self, uid, pid, qry, duration):
        insert_sql = "INSERT INTO user_clicks VALUES ({}, '{}', '{}', {})".format(
            uid, pid, qry, duration)
        cursor = self.__mysql.connection.cursor()
        cursor.execute(insert_sql)
        self.__mysql.connection.commit()
        

