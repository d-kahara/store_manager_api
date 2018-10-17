from flask import request, make_response, jsonify
from datetime import datetime, timedelta
from ....data import Data


class ProductModel():
    """This class encapsulates the functions of the product model"""

    def __init__(self, name, stock, min_q, category, product_id=0):
        """initialize the question model"""
        self.name = name
        self.stock = stock
        self.min_q = min_q
        self.date_created = datetime.now()
        self.category = category
        self.product_id = product_id

    def save_product(self):
        product_id = len(Data.products) + 1
        product = {
            "product_id": product_id,
            "name": self.name,
            "min_q": self.min_q,
            "category": self.category,
            "stock": self.stock,
            "date_created": self.date_created

        }
        #save the product to the products list
        Data.products.append(product)
