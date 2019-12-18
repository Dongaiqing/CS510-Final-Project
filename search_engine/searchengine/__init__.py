from flask import Flask

app = Flask(__name__, 
            static_url_path='', 
            static_folder='static')

# DB config, 'MYSQL_DB' should not be changed
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123123'
app.config['MYSQL_DB'] = 'SearchEngine'

from .engine.db_controller import DBController

db_controller = DBController()

import searchengine.routes