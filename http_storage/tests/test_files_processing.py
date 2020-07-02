import unittest
import os
from http_storage.settings import BASE_DIR
from http_storage.files_processing import simple_hash, get_dir


class TestSimpleHash(unittest.TestCase):

    def setUp(self) -> None:
        self.simple_hash = simple_hash
        self.filename = 'Hello my simple hash'
        self.valid_hash_filename = '43fb3812ab3c9962fd123f678a45c34c34a73a0ab440baa1343f09f1754460d3'

    def test_valid_hash(self):
        self.assertEqual(self.simple_hash(self.filename), self.valid_hash_filename)


class TestGetDir(unittest.TestCase):

    def setUp(self) -> None:
        self.get_dir = get_dir
        self.hashed_filename = '43fb3812ab3c9962fd123f678a45c34c34a73a0ab440baa1343f09f1754460d3'
        self.valid_dir = os.path.join(BASE_DIR, 'store', '43')

    def test_valid_path(self):
        self.assertEqual(self.get_dir(self.hashed_filename), self.valid_dir)


if __name__ == '__main__':
    unittest.main()
