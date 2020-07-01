from http_storage.views import index, upload, upload_handler, download_handler, remove_handler
from aiohttp import web


def setup_routes(app):
    app.add_routes([web.get('/', index),
                    web.get('/upload', upload),
                    web.post('/upload', upload_handler),
                    web.get('/download', download_handler),
                    web.delete('/delete', remove_handler),
                    web.get('/delete', remove_handler)])
