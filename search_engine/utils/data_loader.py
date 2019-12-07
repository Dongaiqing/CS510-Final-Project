import shutil
from os import listdir, mkdir
from os.path import isfile, join, dirname, abspath, exists
from utils import os_directory
import requests
import kaggle

URL = "https://docs.google.com/uc?export=download"

class KaggleLoader:
    def __init__(self,
                 dataset_name="gspmoreira/news-portal-user-interactions-by-globocom",
                 data_path="/../data/kaggle/",
                 unzip=True):
        self.data_path = data_path
        self.dataset_name = dataset_name
        self.unzip = unzip

        self.data_dir = os_directory.safe_dir(dirname(dirname(abspath(__file__)))+self.data_path)

    # returns number of data files in data path
    def load_data(self, test=False):
        if not exists(self.data_dir):
            mkdir(self.data_dir)

        # checks for data having been loaded already first
        onlyfiles = [f for f in listdir(self.data_dir) if isfile(join(self.data_dir, f))]
        if len(onlyfiles) >= 3:
            print("data files already exist in", self.data_dir)
            return

        kaggle.api.authenticate()  # https://www.kaggle.com/docs/api
        print("loading kaggle dataset from", self.dataset_name,"to destination:", self.data_dir)
        kaggle.api.dataset_download_files(self.dataset_name, path=self.data_dir, unzip=self.unzip)


class DataLoader:
    def __init__(self,
                 drive_id="10UBBDPJ37u6JvVPMK1OkGfEWGM-GwEOz",
                 data_path="/../data",
                 destination_filename='grobid_processed.tar.gz'):
        self.drive_id = drive_id
        self.data_path = data_path
        self.destination_filename = destination_filename

        self.data_dir = os_directory.safe_dir(dirname(dirname(abspath(__file__)))+self.data_path)
        self.drive_data = os_directory.safe_dir(dirname(dirname(abspath(__file__)))+self.data_path+'/'+self.destination_filename)
        self.destination_dir = os_directory.safe_dir(dirname(dirname(abspath(__file__)))+self.data_path+'/'+self.destination_filename.split('.')[0]+'/')

    # returns number of data files in data path
    # if no files exist in that path, download and extract the grobid dataset to that directory
    def load_data(self, test=False):
        if not exists(self.data_dir):
            mkdir(self.data_dir)
        if not exists(self.destination_dir):
            mkdir(self.destination_dir)

        # checks for data having been loaded already first
        onlyfiles = [f for f in listdir(self.destination_dir) if isfile(join(self.destination_dir, f))]
        if len(onlyfiles) > 10:
            print(len(onlyfiles), "data files already exist in", self.destination_dir)
            return len(onlyfiles)

        # checks if tgz is already downloaded from Google Drive
        if exists(self.drive_data):
            print("tgz already downloaded")
        else:
            print("downloading tgz from Drive link with id=", self.drive_id)
            if not test:
                self.download_file_from_google_drive(self.drive_id, self.drive_data)

        # extracts files from tgz in place
        print("extracting files from", self.drive_data)
        if not test:
            shutil.unpack_archive(self.drive_data, self.data_dir)
        onlyfiles = [f for f in listdir(self.destination_dir) if isfile(join(self.destination_dir, f))]
        print("extracted", len(onlyfiles), "files to", self.destination_dir)
        return len(onlyfiles)

    def download_file_from_google_drive(self, id, destination):
        session = requests.Session()
        response = session.get(URL, params = { 'id' : id }, stream = True)
        token = self.get_confirm_token(response)

        if token:
            params = { 'id' : id, 'confirm' : token }
            response = session.get(URL, params = params, stream = True)

        self.save_response_content(response, destination)

    def get_confirm_token(self, response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def save_response_content(self, response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)


def csvParse(file):
    out = []
    with open(file) as f:
        for line in f:
            out.append(line.split(','))
    return out


if __name__ == '__main__':
    loader = DataLoader()
    loader.load_data(False)