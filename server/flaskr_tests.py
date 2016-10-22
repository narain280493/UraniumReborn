import os
from app import app as flaskApp
from app import init_db
import unittest
import tempfile


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, flaskApp.config['DATABASE'] = tempfile.mkstemp()
        flaskApp.config['TESTING'] = True
        self.app = flaskApp.test_client()
        with flaskApp.app_context():
            init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskApp.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'alongside graduate students' in rv.data

if __name__ == "__main__":
    unittest.main()
