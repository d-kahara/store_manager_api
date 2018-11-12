import unittest
from flask import json
from app import create_app
from app.tests.v2.base_test import BaseTestCase

sale_endpoint = "api/v2/sales"



class Testsale(BaseTestCase):
    data = {
        "quantity": 1

    }
    product_data = {
        "product_name": "wikO",
        "inventory": 10,
        "category": "phoNes",
        "min_quantity": 0,
        "price": 10000
    }

    category_data = {
        "category_name": "phones"
    }
    def test_create_sale(self):
        """Test for sale creation endpoint."""
        #In order to make a sale, the product has to exist
        data = self.create_admin_test_user()
        authentication_token = data['Authorization']
        self.app.post("api/v2/categories",
                      headers=dict(Authorization=authentication_token),
                      data=json.dumps(self.category_data),
                      content_type='application/json')
        res = self.app.post("api/v2/products",
                            headers=dict(Authorization=authentication_token),
                            data=json.dumps(self.product_data),
                            content_type='application/json')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'successfully created.')
        self.assertEqual(res.status_code, 201)

        data = self.create_test_user()
        authentication_token = data['Authorization']
        res = self.app.post("api/v2/carts/{}".format(1),
                            headers=dict(Authorization=authentication_token),
                            data=json.dumps(self.data),
                            content_type='application/json')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'cart posted successfully.')
        self.assertEqual(res.status_code, 201)
        res = self.app.post("api/v2/sales/",
                            headers=dict(Authorization=authentication_token),
                            content_type='application/json')
        result = json.loads(res.data.decode())
        self.assertEqual(result['Message'], 'Sale Order created.')
        self.assertEqual(res.status_code, 200)

    def test_get_all_sales(self):
        """Test for  get all sales endpoint."""
        data = self.create_admin_test_user()
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
        data = self.create_admin_test_user()
        authentication_token = data['Authorization']
        res = self.app.get(sale_endpoint,
                           headers=dict(Authorization=authentication_token),
                           )
        self.assertEqual(res.status_code, 200)

    def test_get_sale_by_email(self):
        """Test for get sale by id endpoint."""
        #To test we need to create a category, then product then get the product
        data = self.create_admin_test_user()
        authentication_token = data['Authorization']
        self.app.post("api/v2/categories",
                      headers=dict(Authorization=authentication_token),
                      data=json.dumps(self.category_data),
                      content_type='application/json')
        res = self.app.post("api/v2/products",
                            headers=dict(Authorization=authentication_token),
                            data=json.dumps(self.product_data),
                            content_type='application/json')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'successfully created.')
        self.assertEqual(res.status_code, 201)
        res = self.app.post("api/v2/carts/{}".format(1),
                            headers=dict(Authorization=authentication_token),
                            data=json.dumps(self.data),
                            content_type='application/json')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'cart posted successfully.')
        self.assertEqual(res.status_code, 201)
        res = self.app.post("api/v2/sales/",
                            headers=dict(Authorization=authentication_token),
                            content_type='application/json')
        result = json.loads(res.data.decode())
        self.assertEqual(result['Message'], 'Sale Order created.')
        self.assertEqual(res.status_code, 200)
        #Now retrieve the product
        res = self.app.get("/api/v2/sales/{}".format('admin@gmail.com'),
                           headers=dict(Authorization=authentication_token),
                           )
        self.assertEqual(res.status_code, 200)

    def test_get_sale_that_does_not_exist(self):
        """Test for the get sale by id endpoint."""
        data = self.create_test_user()
        authentication_token = data['Authorization']
        sale_id = 1759
        res = self.app.get("/api/v2/sales/{}".format(sale_id),
                           headers=dict(Authorization=authentication_token),
                           )
        self.assertEqual(res.status_code, 404)
