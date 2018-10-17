"""This class will contain test configurations"""
from flask_testing import TestCase
import json
import unittest

from run import app
from ...data import Data
from instance.config import app_config


class BaseTestCase(unittest.TestCase):
    """Base Tests"""

    def create_app(self):
        app.config.from_object(app_config["testing"])
        app.config.from_pyfile('config.py')
        return app

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        

    def tearDown(self):
      Data.products = []
      Data.sales = []
