"""This class will contain test configurations"""
import json
import unittest

from run import app
from ...data import Data
from instance.config import app_config

reg_endpoint = "api/v1/auth/register"

#Login endpoint
login_endpoint = "api/v1/auth/login"

class BaseTestCase(unittest.TestCase):
    """Base Tests"""

    user_data = {
        "email": "hash@mail.com",
        "password": "password123",
        "admin": False

    }
    admin_user_data_reg = {
        "email": "admin@mail.com",
        "password": "password123",
        "admin": True
    }
    admin_user_data = {
        "email": "admin@mail.com",
        "password": "password123",
        "admin": True
    }

    def create_app(self):
        app.config.from_object(app_config["testing"])
        app.config.from_pyfile('config.py')
        return app

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        
        

    def tearDown(self):
      Data.products.clear()
      Data.sales.clear()
      Data.users.clear()

    def create_test_user(self):
        user_response = self.app.post(reg_endpoint,
                                      data=json.dumps(self.user_data),
                                      content_type='application/json')
        self.assertEqual(user_response.status_code, 201)

        # registered user login
        login_response = self.app.post(login_endpoint,
                                       data=json.dumps(self.user_data),
                                       content_type='application/json')
        data = json.loads(login_response.data.decode())
        self.assertTrue(data['Authorization'])
        self.assertEqual(login_response.status_code, 200)
        return data
        
    def create_admin_test_user(self):
        user_response = self.app.post(reg_endpoint,
                                      data=json.dumps(self.admin_user_data_reg),
                                      content_type='application/json')
        self.assertEqual(user_response.status_code, 201)

        # registered user login
        login_response = self.app.post(login_endpoint,
                                       data=json.dumps(self.admin_user_data),
                                       content_type='application/json')
        data = json.loads(login_response.data.decode())
        self.assertTrue(data['Authorization'])
        self.assertEqual(login_response.status_code, 200)
        return data
