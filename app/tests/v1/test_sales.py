import unittest
from flask import json
from app import create_app
from app.tests.v1.base_test import BaseTestCase

sale_endpoint = "api/v1/sales"


class Testsale(BaseTestCase):
    data = {
        "cart_total": 1030,
        "posted_by": "Shantel",
        "cart_id": 10
    }

    def test_create_sale(self):
        """Test for sale creation endpoint."""
        res = self.app.post(sale_endpoint,
                            data=json.dumps(self.data),
                            content_type='application/json')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'success')
        self.assertEqual(res.status_code, 201)

    def test_get_all_sales(self):
        """Test for  get all sales endpoint."""
        self.app.post(sale_endpoint,
                      data=json.dumps(self.data),
                      content_type='application/json')
        res = self.app.get(sale_endpoint)
        self.assertEqual(res.status_code, 200)

    def test_empty_database(self):
        """Test sales database if empty."""
        res = self.app.get(sale_endpoint)
        self.assertEqual(res.status_code, 404)

    def test_get_sale_by_id(self):
        """Test for get sale by id endpoint."""
        self.app.post(sale_endpoint,
                      data=json.dumps(self.data),
                      content_type='application/json')
        sale_id = 1
        res = self.app.get("/api/v1/sales/{}".format(sale_id))
        self.assertEqual(res.status_code, 200)

    def test_get_sale_that_does_not_exist(self):
        """Test for the get sale by id endpoint."""
        sale_id = 17599898
        res = self.app.get("/api/v1/sales/{}".format(sale_id))
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
