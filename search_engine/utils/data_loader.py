import shutil
from os import listdir, mkdir
from os.path import isfile, join, dirname, abspath, exists
import os_directory
import requests

URL = "https://docs.google.com/uc?export=download"

class DataLoader():
    # returns number of data files in data path
    # if no files exist in that path, download and extract the grobid dataset to that directory
    def load_data(self,
                  drive_id="10UBBDPJ37u6JvVPMK1OkGfEWGM-GwEOz",
                  data_path="/../data",
                  destination_filename='grobid_processed.tar.gz'):
        # init variables, ensure data path exists
        data_dir = os_directory.safe_dir(dirname(dirname(abspath(__file__)))+data_path)
        drive_data = os_directory.safe_dir(dirname(dirname(abspath(__file__)))+data_path+'/'+destination_filename)
        destination_dir = os_directory.safe_dir(dirname(dirname(abspath(__file__)))+data_path+'/'+destination_filename.split('.')[0])
        if not exists(data_dir):
            mkdir(data_dir)
        if not exists(destination_dir):
            mkdir(destination_dir)

        # checks for data having been loaded already first
        onlyfiles = [f for f in listdir(destination_dir) if isfile(join(destination_dir, f))]
        if len(onlyfiles) > 10:
            print(len(onlyfiles), "data files already exist in", destination_dir)
            return len(onlyfiles)

        # checks if tgz is already downloaded from Google Drive
        if exists(drive_data):
            print("tgz already downloaded")
        else:
            print("downloading tgz from Drive link with id=", drive_id)
            self.download_file_from_google_drive(drive_id, drive_data)

        # extracts files from tgz in place
        print("extracting files from", drive_data)
        shutil.unpack_archive(drive_data, data_dir)
        onlyfiles = [f for f in listdir(destination_dir) if isfile(join(destination_dir, f))]
        print("extracted", len(onlyfiles), "files to", destination_dir)

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

if __name__ == '__main__':
    loader = DataLoader()
    loader.load_data()