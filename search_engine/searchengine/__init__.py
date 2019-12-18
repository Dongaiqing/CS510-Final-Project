from flask import Flask

app = Flask(__name__, 
            static_url_path='', 
            static_folder='static')

# DB config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123123'
app.config['MYSQL_DB'] = 'SearchEngine'

# from utils import os_directory
# from utils.data_loader import DataLoader
# from searchengine.engine.model import UnigramLM
from .engine.db_controller import DBController
# loader = DataLoader()
# num_files = loader.load_data()
# model = UnigramLM(loader.destination_dir, num_files, 0.1)

db_controller = DBController()

import searchengine.routes