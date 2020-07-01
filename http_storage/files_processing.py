import hashlib
import os
from datetime import datetime
from http_storage.settings import BASE_DIR
import aiohttp


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


async def file_writer(hashed_filename: str, file_object) -> str:
    file_store_path = get_dir(hashed_filename)
    with open(os.path.join(file_store_path, hashed_filename), 'wb') as file:
        while True:
            chunk = await file_object.read_chunk()
            if not chunk:
                break
            file.write(chunk)
    return hashed_filename


@aiohttp.streamer
async def file_sender(writer, file_store_path: str):
    chunk_size = 2 ** 16
    with open(file_store_path, 'rb') as file:
        chunk = file.read(chunk_size)
        while chunk:
            await writer.write(chunk)
            chunk = file.read(chunk_size)


def file_remover(hashed_filename: str):
    file_store_path = get_dir(hashed_filename)
    os.remove(os.path.join(file_store_path, hashed_filename))
