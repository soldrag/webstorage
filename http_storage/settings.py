import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / 'http_storage' / 'config' / 'http_storage.yml'


def get_config(path):
    with open(path) as file:
        cfg = yaml.safe_load(file)
    return cfg


config = get_config(CONFIG_PATH)
