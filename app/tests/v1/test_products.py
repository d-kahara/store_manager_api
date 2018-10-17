import unittest
from flask import json
from app import create_app
from app.tests.v1.base_test import BaseTestCase

prod_endpoint = "api/v1/products"


class TestProduct(BaseTestCase):
    data = {
        "stock": 980,
        "min_q": 145,
        "name": "Pepsi",
        "category": "Bevarages"
    }

    def test_create_product(self):
        """Test for product creation endpoint."""
        res = self.app.post("api/v1/products",
                            data=json.dumps(self.data),
                            content_type='application/json')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'success')
        self.assertEqual(res.status_code, 201)

    def test_get_all_products(self):
        """Test for  get all products endpoint."""
        self.app.post(prod_endpoint,
                      data=json.dumps(self.data),
                      content_type='application/json')
        res = self.app.get(prod_endpoint)
        self.assertEqual(res.status_code, 200)

    def test_empty_database(self):
        """Test products database if empty."""
        res = self.app.get(prod_endpoint)
        self.assertEqual(res.status_code, 404)

    def test_get_product_by_id(self):
        """Test for get product by id endpoint."""
        self.app.post(prod_endpoint,
                      data=json.dumps(self.data),
                      content_type='application/json')
        product_id = 1
        res = self.app.get("/api/v1/products/{}".format(product_id))
        self.assertEqual(res.status_code, 200)

    def test_get_product_that_does_not_exist(self):
        """Test for the get product by id endpoint."""
        product_id = 1759
        res = self.app.get("/api/v1/products/{}".format(product_id))
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
