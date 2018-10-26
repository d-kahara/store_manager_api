"""This class will contain test configurations"""
import json
import unittest
import os
import psycopg2

from run import app
from ...data import Data
from instance.config import app_config
from app import create_app

reg_endpoint = "api/v2/auth/register"

#Login endpoint
login_endpoint = "api/v2/auth/login"


class BaseTestCase(unittest.TestCase):
    """Base Tests"""

    user_data = {
        "email": "hash@mail.com",
        "password": "password123",
        "role": "Admin"

    }
    admin_user_data_reg = {
        "email": "admin@mail.com",
        "password": "password123",
        "role": "Admin"
    }
    admin_user_data = {
        "email": "admin@mail.com",
        "password": "password123",
        "role": "Admin"
    }

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.app = app.test_client()



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
                                      data=json.dumps(
                                          self.admin_user_data_reg),
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

    def tearDown(self):
        DATABASE_URI = app_config['testing'].DATABASE_URI
        conn = psycopg2.connect(DATABASE_URI)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE users, products, blacklist")
        conn.commit()
        conn.close()
