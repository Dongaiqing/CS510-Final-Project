import os

def safe_dir(dir_path):
    if os.name == 'nt':
        return dir_path.replace('/', '\\')
    else:
        return dir_path.replace('\\', '/')