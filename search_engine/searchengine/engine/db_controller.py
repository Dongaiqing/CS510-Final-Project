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
        click_score = 0
        if duration >= 5 and duration < 15:
            click_score = 1
        else:
            click_score = 2

        insert_sql = "INSERT INTO rel_scores VALUES ({}, '{}', '{}', {}, DEFAULT) ON DUPLICATE KEY UPDATE click_score = {}".format(
            uid, pid, qry, click_score, click_score)
        cursor = self.__mysql.connection.cursor()
        cursor.execute(insert_sql)
        self.__mysql.connection.commit()

    def record_user_rel_sel(self, uid, pid, qry, rel):
        rel_score = 0 if rel == 0 else 2
        insert_sql = "INSERT INTO rel_scores VALUES ({}, '{}', '{}', DEFAULT, {}) ON DUPLICATE KEY UPDATE rel_score = {}".format(
            uid, pid, qry, rel_score, rel_score)
        cursor = self.__mysql.connection.cursor()
        cursor.execute(insert_sql)
        self.__mysql.connection.commit()
        
    def get_user_rel_scores(self, uid, query, pid=None):
        if pid is None:
            fetch_sql = "SELECT p_id, rel_score + click_score AS score FROM rel_scores WHERE u_id = {} AND qry = '{}'".format(uid, query)
            cursor = self.__mysql.connection.cursor()
            cursor.execute(fetch_sql)
            data = cursor.fetchall()
            return None if len(data) == 0 else data
        else:
            fetch_sql = "SELECT rel_score + click_score AS score FROM rel_scores WHERE u_id = {} AND p_id = '{}' AND qry = '{}'".format(uid, pid, query)
            cursor = self.__mysql.connection.cursor()
            cursor.execute(fetch_sql)
            data = cursor.fetchone()
            return None if data is None else data[0]