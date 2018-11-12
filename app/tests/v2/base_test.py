"""This class will contain test configurations"""
import json
import unittest
import os
import psycopg2

from werkzeug.security import generate_password_hash
from datetime import datetime

from run import app
from ...data import Data
from instance.config import app_config
from app import create_app
from ...api.v2.utils.db_helper import init_db

reg_endpoint = "api/v2/auth/register"

#Login endpoint
login_endpoint = "api/v2/auth/login"


class BaseTestCase(unittest.TestCase):
    """Base Tests"""

    user_data = {
        "email": "hash@mail.com",
        "password": "password123",
        "role": "Attendant"

    }

    user_data_login = {
        "email": "hash@mail.com",
        "password": "password123"
    }

    admin_user_data = {
        "email": "admin@gmail.com",
        "password": "password123",
    }

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.app = app.test_client()

        self.db = init_db()
        curr = self.db.cursor()
        new_user = dict(
            role='admin',
            email='admin@gmail.com',
            registered_on=datetime.now(),
            password=generate_password_hash('password123')
        )
        sql = """INSERT INTO users (role,email, registered_on, password) \
            VALUES ( %(role)s, %(email)s, %(registered_on)s, %(password)s);
            """
        
        curr.execute(sql, new_user)
        self.db.commit()
        curr.close()


    def create_test_user(self):
        #admin Logs in
        login_response = self.app.post(login_endpoint,
                                data=json.dumps(self.admin_user_data),
                                content_type='application/json')
        data = json.loads(login_response.data.decode())
        self.assertEqual(login_response.status_code, 200)
        admin_token = data['Authorization']
        
        #Admin creates user
        user_response = self.app.post(reg_endpoint,
                                      headers=dict(
                                          Authorization=admin_token),
                                      data=json.dumps(self.user_data),
                                      content_type='application/json')
        self.assertEqual(user_response.status_code, 201)

        # registered user login
        login_response = self.app.post(login_endpoint,
                                       data=json.dumps(self.user_data_login),
                                       content_type='application/json')
        data = json.loads(login_response.data.decode())
        self.assertTrue(data['Authorization'])
        self.assertEqual(login_response.status_code, 200)
        return data

    def create_admin_test_user(self):
        # admin login
        login_response = self.app.post(login_endpoint,
                                       data=json.dumps(self.admin_user_data),
                                       content_type='application/json')
        data = json.loads(login_response.data.decode())
     
        self.assertTrue(data['Authorization'])
        self.assertEqual(login_response.status_code, 200)
        return data

    def tearDown(self):
        DATABASE_URL = app_config['testing'].DATABASE_URL
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE users cascade;")
        cursor.execute("DROP TABLE categories cascade;")
        cursor.execute("DROP TABLE sales cascade;")        
        cursor.execute("DROP TABLE products cascade;")        
        cursor.execute("DROP TABLE blacklist cascade;")        
        cursor.execute("DROP TABLE carts cascade;")        


        conn.commit()
        conn.close()
