import os
from database.database import init_db
import app
import unittest
import tempfile


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.app.test_client()
        with app.app.app_context():
            init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def test_without_login(self):
        rv_root = self.app.get("/")
        assert b'<body class="loginbody"' in rv_root.data
        rv_lp = self.app.get("/listofprojects", follow_redirects=True)
        assert b'<body class="loginbody"' in rv_lp.data
        rv_fac = self.app.get("/faculty", follow_redirects=True)
        assert b'<body class="loginbody"' in rv_fac.data
        rv_stud = self.app.get("/student", follow_redirects=True)
        assert b'<body class="loginbody"' in rv_stud.data

    def test_signup(self):
        rv = self.app.post("/signup", data=dict(
            first_name="testFirst",
            last_name="testLast",
            email="test@colorado.edu",
            password="testpwd"
        ), follow_redirects=True)
        if b'Create your account' not in rv.data:
            assert b'Whether helping develop new diagnostic techniques' in rv.data

    def test_login(self):
        return self.app.post("/login", data=dict(
            useremail="test@colorado.edu",
            password="testpwd"
        ), follow_redirects=True)

    def test_home_page(self):
        rv_login = self.test_login()
        assert b'Whether helping develop new diagnostic techniques' in rv_login.data
        rv = self.app.get("/")
        assert b'Whether helping develop new diagnostic techniques' in rv.data

    def test_post_request(self):
        rv_login = self.test_login()
        assert b'Whether helping develop new diagnostic techniques' in rv_login.data
        self.app.post("/listofprojects",
                           data=dict(facultyFirstName="test_db_first_name", facultyLastName="test_db_last_name"))
        rv = self.app.get("/listofprojects")
        assert b'test_db_first_name' in rv.data
        assert b'test_db_last_name' in rv.data


if __name__ == '__main__':
    unittest.main()
