import aiohttp_jinja2
import jinja2
import logging
from aiohttp import web
from http_storage.routes import setup_routes
from http_storage.settings import BASE_DIR, config


SRV_HOST, SRV_PORT = config['server'].values()

if __name__ == '__main__':
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(f'{BASE_DIR}/http_storage/templates'))
    setup_routes(app)
    # logging.basicConfig(level=logging.DEBUG)
    web.run_app(app, host=SRV_HOST, port=SRV_PORT)
