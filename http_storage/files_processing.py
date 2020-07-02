import hashlib
import os
from datetime import datetime
from http_storage.settings import BASE_DIR
import aiohttp


STORE_DIR_NAME = 'store'


def simple_hash(file_name: str) -> str:
    """
    Simple hashing, return sha256 hash of filename
    """
    return hashlib.sha256(file_name.encode('utf8')).hexdigest()


def unique_hash(file_name: str) -> str:
    """
    Unique hashing, return sha256 hash of filename+timestamp
    """
    timestamp = datetime.timestamp(datetime.now())
    unique_name = f'{file_name}.{str(timestamp)}'
    return hashlib.sha256(unique_name.encode('utf8')).hexdigest()


def get_dir(hashed_filename: str) -> str:
    """
    :return: directory for file, /store/{2 first symbols of name}
    """
    file_store_path = os.path.join(BASE_DIR, STORE_DIR_NAME, hashed_filename[:2])
    if not os.path.exists(file_store_path):
        os.mkdir(file_store_path)
    return file_store_path


async def file_writer(hashed_filename: str, file_object) -> str:
    """
    Write file in storage.
    """
    file_store_path = get_dir(hashed_filename)
    with open(os.path.join(file_store_path, hashed_filename), 'wb') as file:
        while True:
            chunk = await file_object.read_chunk()
            if not chunk:
                break
            file.write(chunk)
    return hashed_filename


@aiohttp.streamer
async def file_sender(writer, file_store_path: str) -> None:
    """
    Write file in stream
    """
    chunk_size = 2 ** 16
    with open(file_store_path, 'rb') as file:
        chunk = file.read(chunk_size)
        while chunk:
            await writer.write(chunk)
            chunk = file.read(chunk_size)


async def file_remover(hashed_filename: str) -> None:
    """
    Remove file from storage
    """
    file_store_path = get_dir(hashed_filename)
    os.remove(os.path.join(file_store_path, hashed_filename))
