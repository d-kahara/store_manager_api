import unittest
import json
from app.tests.v2.base_test import BaseTestCase

#Registration endpoint
reg_endpoint = "api/v2/auth/register"

#Login endpoint
login_endpoint = "api/v2/auth/login"

#Logout endpoint
logout_endpoint = "api/v2/auth/logout"


class TestAuthBlueprint(BaseTestCase):

    data = {
        "email": "hash@mail.com",
        "password": "password123",
        "role": "Attendant"

    }

    data_bad_email = {
        "email": "worldstar.",
        "password": "pass",
        "role": "Attendant"
    }

    data_no_pass = {
        "email": "hash@mail.com",
        "role": "Attendant"
    }

    data_wrong_pass = {
        "email": "hash@mail.com",
        "password": "you_know_im_bad_",
        "role": "Attendant"
    }

    def test_user_registration(self):
        """Test that user can register successfully"""
        data = self.create_admin_test_user()
        admin_token=data['Authorization']
        user_reg = self.app.post(reg_endpoint,
                                 headers=dict(
                                     Authorization=admin_token),
                                 data=json.dumps(self.data),
                                 content_type='application/json')
        response = json.loads(user_reg.data.decode())
        self.assertEqual(response['message'],
                         'Successfully registered. You can now log in')
        self.assertEqual(user_reg.status_code, 201)

    def test_registered_user_login(self):
        """ Test for login of registered-user  """
        data = self.create_admin_test_user()
        admin_token = data['Authorization']
        user_response = self.app.post(reg_endpoint,
                                         headers=dict(
                                     Authorization=admin_token),
                                      data=json.dumps(self.data),
                                      content_type='application/json')
        self.assertEqual(user_response.status_code, 201)

        # registered user login
        login_response = self.app.post(login_endpoint,
                                       data=json.dumps(self.data),
                                       content_type='application/json')
        data = json.loads(login_response.data.decode())
        self.assertTrue(data['Authorization'])
        self.assertEqual(login_response.status_code, 200)

    def test_valid_logout(self):
        """ Test for logout before token expires """
        # user registration
        data = self.create_admin_test_user()
        admin_token = data['Authorization']
        user_reg = self.app.post(reg_endpoint,
                                 headers=dict(
                                     Authorization=admin_token),
                                 data=json.dumps(self.data),
                                 content_type='application/json')
        response = json.loads(user_reg.data.decode())
        self.assertEqual(response['message'],
                         'Successfully registered. You can now log in')
        self.assertEqual(user_reg.status_code, 201)

        # registered user login
        login_response = self.app.post(login_endpoint,
                                       data=json.dumps(self.data),
                                       content_type='application/json')
        data = json.loads(login_response.data.decode())
        self.assertTrue(data['Authorization'])
        self.assertEqual(login_response.status_code, 200)
        auth_token = data['Authorization']

        # valid token logout
        response = self.app.post(
            logout_endpoint,
            headers=dict(
                Authorization=auth_token
            )
        )
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], 'Successfully logged out.')
        self.assertEqual(response.status_code, 200)

    def test_empty_password_registration(self):
        """Test registration without password"""
        data = self.create_admin_test_user()
        admin_token = data['Authorization']
        user_reg = self.app.post(reg_endpoint,
                                 headers=dict(
                                     Authorization=admin_token),
                                 data=json.dumps(self.data_no_pass),
                                 content_type='application/json')
        response = json.loads(user_reg.data.decode())
        errors = response['errors']
        self.assertEqual(errors['password'],
                         "\'password\' is a required property")
        self.assertEqual(user_reg.status_code, 400)

    def test_existing_user(self):
        """Test that user cant register twice"""
        # user registration
        data = self.create_admin_test_user()
        admin_token = data['Authorization']
        user_reg = self.app.post(reg_endpoint,
                                 headers=dict(
                                     Authorization=admin_token),
                                 data=json.dumps(self.data),
                                 content_type='application/json')
        response = json.loads(user_reg.data.decode())
        self.assertEqual(response['message'],
                         'Successfully registered. You can now log in')
        self.assertEqual(user_reg.status_code, 201)

        user_reg2 = self.app.post(reg_endpoint,
                                  headers=dict(
                                      Authorization=admin_token),
                                  data=json.dumps(self.data),
                                  content_type='application/json')
        response2 = json.loads(user_reg2.data.decode())
        self.assertEqual(user_reg2.status_code, 403)
        self.assertEqual(response2['message'],
                         'User already exists.Please log in to continue.')

    def test_invalid_login_password(self):
        """Test that user cant login with a wrong  password"""
        #Registration of user
        data = self.create_admin_test_user()
        admin_token = data['Authorization']
        user_reg = self.app.post(reg_endpoint,
                                 headers=dict(
                                     Authorization=admin_token),
                                 data=json.dumps(self.data),
                                 content_type='application/json')
        response = json.loads(user_reg.data.decode())
        self.assertEqual(response['message'],
                         'Successfully registered. You can now log in')
        self.assertEqual(user_reg.status_code, 201)
        #Login user
        user_login = self.app.post(login_endpoint,
                                   data=json.dumps(self.data_wrong_pass),
                                   content_type='application/json')
        response = json.loads(user_login.data.decode())
        self.assertEqual(response['message'],
                         'Invalid login credentials.Please try again')
        self.assertEqual(user_login.status_code, 401)

    def test_login_blank_password(self):
        """Test that user cant login without password"""
        data = self.create_admin_test_user()
        admin_token = data['Authorization']
        #Resgistration
        user_reg = self.app.post(reg_endpoint,
                                 headers=dict(
                                     Authorization=admin_token),
                                 data=json.dumps(self.data),
                                 content_type='application/json')
        response = json.loads(user_reg.data.decode())
        self.assertEqual(response['message'],
                         'Successfully registered. You can now log in')
        #Login user
        user_login = self.app.post(login_endpoint,
                                   data=json.dumps(self.data_no_pass),
                                   content_type='application/json')
        response = json.loads(user_login.data.decode())
        error = response["errors"]
        self.assertEqual(error['password'],
                         "\'password\' is a required property")
        self.assertEqual(user_login.status_code, 400)

    def test_login_unregistered_account(self):
        # unregistered user login
        login_response = self.app.post(login_endpoint,
                                       data=json.dumps(self.data),
                                       content_type='application/json')
        self.assertEqual(login_response.status_code, 404)

    def test_invalid_email(self):
        """Test that user cant use invalid email"""
        data = self.create_admin_test_user()
        admin_token = data['Authorization']
        user_reg = self.app.post(reg_endpoint,
                                 headers=dict(
                                     Authorization=admin_token),
                                 data=json.dumps(self.data_bad_email),
                                 content_type='application/json')
        response = json.loads(user_reg.data.decode())
        self.assertEqual(user_reg.status_code, 400)
        self.assertEqual(
            response['message'], 'Invalid Email format.Email has to be of the form \'example@example.com\'.')
        user_login = self.app.post(login_endpoint,
                                   data=json.dumps(self.data_bad_email),
                                   content_type='application/json')
        response = json.loads(user_login.data.decode())
        self.assertEqual(
            response['message'], 'Invalid Email format.Email has to be of the form \'example@example.com\'.')
        self.assertEqual(user_login.status_code, 400)

    def test_token_creation(self):
        """Test that auth token is created when a user logs in"""

        data = self.create_test_user()
        authentication_token = data['Authorization']
        self.assertTrue(authentication_token)

