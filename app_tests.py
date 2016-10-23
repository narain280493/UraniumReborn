import os
from database.database import init_db
import app
import unittest
import tempfile


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        with app.app.app_context():
            init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def test_home_page(self):
        rv = self.app.get("/")
        assert b'Whether helping develop new diagnostic techniques' in rv.data

    def test_post_request(self):
        self.app.post("/listofprojects",
                           data=dict(facultyFirstName="test_db_first_name", facultyLastName="test_db_last_name"))
        rv = self.app.get("/listofprojects")
        assert b'test_db_first_name' in rv.data
        assert b'test_db_last_name' in rv.data


if __name__ == '__main__':
    unittest.main()
