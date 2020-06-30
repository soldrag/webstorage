from aiohttp import web
from routes import setup_routes
from settings import BASE_DIR
import aiohttp_jinja2
import jinja2

app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(f'{BASE_DIR}/http_storage/templates'))
setup_routes(app)
web.run_app(app)
