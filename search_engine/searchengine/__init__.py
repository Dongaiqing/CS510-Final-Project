from flask import Flask

app = Flask(__name__, 
            static_url_path='', 
            static_folder='static')

from utils import os_directory
from utils.data_loader import DataLoader
from searchengine.engine.model import UnigramLM

loader = DataLoader()
num_files = loader.load_data()
model = UnigramLM(loader.destination_dir, num_files, 0.1)

from searchengine import routes