from flask import Flask
from flask_testing import TestCase


class ServerTests(TestCase):
    def create_app(self):
        tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
        app = Flask('UraniumReborn', template_folder=tmpl_dir)
        app.config['TESTING'] = True
