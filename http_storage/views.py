import aiohttp_jinja2
from aiohttp import web
import os
from http_storage.files_processing import file_writer, unique_hash, get_dir, simple_hash, file_sender, file_remover
from http_storage.settings import config


HASH_TYPE = config['http_storage']['hash_type']


@aiohttp_jinja2.template('upload.html')
async def upload(request):
    pass


async def upload_handler(request) -> web.json_response:
    print(request.headers)
    reader = await request.multipart()
    field = await reader.next()
    assert field.name == 'file'
    filename = field.filename

    hashed_filename = unique_hash(filename) if HASH_TYPE else simple_hash(filename)

    await file_writer(hashed_filename, field)
    return web.json_response({'status': 'uploaded', 'file_id': hashed_filename})


async def download_handler(request) -> web.json_response:
    hashed_filename = request.query['file_id']
    file_store_path = os.path.join(get_dir(hashed_filename), hashed_filename)
    if os.path.exists(file_store_path):
        headers = {f'Content-disposition': f'attachment; filename={hashed_filename}'}
        return web.Response(body=file_sender(file_store_path=file_store_path), headers=headers, status=200)
    else:
        return web.json_response({'file_id': hashed_filename, 'status': 'file not found.'})


async def remove_handler(request) -> web.json_response:
    hashed_filename = request.query['file_id']
    try:
        await file_remover(hashed_filename)
        return web.json_response({'file_id': hashed_filename, 'status': 'file deleted.'})
    except FileNotFoundError:
        return web.json_response({'file_id': hashed_filename, 'status': 'file not found.'})
