import hashlib
import os
from datetime import datetime
from http_storage.settings import BASE_DIR


STORE_DIR_NAME = 'store'


def simple_hash(file_name: str) -> str:
    return hashlib.sha256(file_name.encode('utf8')).hexdigest()


def unique_hash(file_name: str) -> str:
    unique_name = f'{file_name}.{str(datetime.timestamp(datetime.now()))}'
    return hashlib.sha256(unique_name.encode('utf8')).hexdigest()


def get_dir(hashed_filename: str) -> str:
    file_store_path = os.path.join(BASE_DIR, STORE_DIR_NAME, hashed_filename[:2])
    if not os.path.exists(file_store_path):
        os.mkdir(file_store_path)
    return file_store_path


def file_writer(hashed_filename, file_store_path, file_object):
    with open(os.path.join(file_store_path, hashed_filename), 'wb') as file:
        file.write(file_object)


def file_reader(hashed_filename: str, file_store_path: str):
    with open(os.path.join(file_store_path, hashed_filename), 'rb') as file:
        file_object = file.read()
    return file_object


def file_remover(hash_filename: str, file_store_path: str):
    os.remove(os.path.join(file_store_path, hash_filename))
