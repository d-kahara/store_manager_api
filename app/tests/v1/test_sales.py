import unittest
from flask import json
from app import create_app
from app.tests.v1.base_test import BaseTestCase

sale_endpoint = "api/v1/sales"
#Registration endpoint
reg_endpoint = "api/v1/auth/register"

#Login endpoint
login_endpoint = "api/v1/auth/login"


class Testsale(BaseTestCase):
    data = {
        "cart_total": 1030,
        "posted_by": "Shantel",
        "cart_id": 10
    }


    def test_create_sale(self):
        """Test for sale creation endpoint."""

        data=self.create_test_user()
        authentication_token = data['Authorization']
        res = self.app.post(sale_endpoint,
         headers=dict(Authorization=authentication_token),
                            data=json.dumps(self.data),
                            content_type='application/json')    
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'success')
        self.assertEqual(res.status_code, 201)
    

    def test_get_all_sales(self):
        """Test for  get all sales endpoint."""
        data = self.create_test_user()
        authentication_token = data['Authorization']
        self.app.post(sale_endpoint,
                      headers=dict(Authorization=authentication_token),
                      data=json.dumps(self.data),
                      content_type='application/json')
        res = self.app.get(sale_endpoint,
                           headers=dict(Authorization=authentication_token),
                           )
        self.assertEqual(res.status_code, 200)

    def test_empty_database(self):
        """Test sales database if empty."""
        data = self.create_test_user()
        authentication_token = data['Authorization']
        res = self.app.get(sale_endpoint,
                           headers=dict(Authorization=authentication_token),
                           )
        self.assertEqual(res.status_code, 404)

    def test_get_sale_by_id(self):
        """Test for get sale by id endpoint."""
        data = self.create_test_user()
        authentication_token = data['Authorization']
        self.app.post(sale_endpoint,
                      headers=dict(Authorization=authentication_token),
                      data=json.dumps(self.data),
                      content_type='application/json')
        sale_id = 1
        res = self.app.get("/api/v1/sales/{}".format(sale_id),
                           headers=dict(Authorization=authentication_token),
        )
        self.assertEqual(res.status_code, 200)

    def test_get_sale_that_does_not_exist(self):
        """Test for the get sale by id endpoint."""
        data = self.create_test_user()
        authentication_token = data['Authorization']
        sale_id = 1759
        res = self.app.get("/api/v1/sales/{}".format(sale_id),
                           headers=dict(Authorization=authentication_token),
                           )
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
