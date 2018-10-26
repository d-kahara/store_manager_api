import unittest
from flask import json
from app import create_app
from app.tests.v2.base_test import BaseTestCase

prod_endpoint = "api/v2/products"


class TestProduct(BaseTestCase):
    data={
        "product_name": "balenciaga",
        "min_quantity": 5,
        "inventory": 10,
        "category": "clothes",
    }

    def test_create_product(self):
        """Test for product creation endpoint."""
        data = self.create_admin_test_user()
        authentication_token = data['Authorization']

        res = self.app.post("api/v2/products",
                            headers=dict(Authorization=authentication_token),
                            data=json.dumps(self.data),
                            content_type='application/json')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'success')
        self.assertEqual(res.status_code, 201)

    def test_get_all_products(self):
        """Test for  get all products endpoint."""

        data = self.create_admin_test_user()
        authentication_token = data['Authorization']
        self.app.post(prod_endpoint,
                      headers=dict(Authorization=authentication_token),
                      data=json.dumps(self.data),
                      content_type='application/json')
        res = self.app.get(prod_endpoint,
                           headers=dict(Authorization=authentication_token),
                           )
        self.assertEqual(res.status_code, 200)

    def test_empty_database(self):
        """Test products database if empty."""
        data = self.create_test_user()
        authentication_token = data['Authorization']
        res = self.app.get(prod_endpoint,
                           headers=dict(Authorization=authentication_token),
                           )
        self.assertEqual(res.status_code, 200)


    def test_get_product_by_id(self):
        """Test for get product by id endpoint."""
        data = self.create_admin_test_user()
        authentication_token = data['Authorization']
        self.app.post(prod_endpoint,
                      headers=dict(Authorization=authentication_token),
                      data=json.dumps(self.data),
                      content_type='application/json')
        product_id = 1
        res = self.app.get("/api/v2/products/{}".format(product_id),
                           headers=dict(Authorization=authentication_token),
                           )
        self.assertEqual(res.status_code, 200)

    def test_get_product_that_does_not_exist(self):
        """Test for the get product by id endpoint."""
        data = self.create_test_user()
        authentication_token = data['Authorization']
        product_id = 1759
        res = self.app.get("/api/v2/products/{}".format(product_id),
                           headers=dict(Authorization=authentication_token),
                           )
        self.assertEqual(res.status_code, 404)
