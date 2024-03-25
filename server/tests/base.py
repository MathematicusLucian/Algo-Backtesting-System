import unittest
from server.src.api import create_app_blueprint
from server.tests import config_name

class BaseTestCase(unittest.TestCase):

    def create_app(self):
        return create_app_blueprint(config_name)

    def setUp(self):
        app = self.create_app()
        self.client = app.test_client(self)
        self.context = app.app_context()
        self.request_context = app.test_request_context()

    def tearDown(self):
        pass
