from datetime import datetime
from werkzeug.exceptions import NotFound
from ..utils.db_helper import init_db
from flask import request
import psycopg2.extras as extras
import psycopg2


class Cart:
    def __init__(self, product_id=0, quantity=0, email='email@e.cm'):
        """
        cart constructor
        # """
        self.product_id = product_id
        self.quantity = quantity
        self.email = email
        self.created_at = datetime.now().replace(second=0, microsecond=0)
        self.db = init_db()


    def post_cart(self, product_id, quantity, email):
          
        curr = self.db.cursor(cursor_factory=extras.DictCursor)
        curr.execute(
            "select * from products where product_id = (%s);", (product_id,))
        product = curr.fetchone()
        if  not product:
            raise NotFound('Product does not exist.')
        product_name = product[7].lower()
        stock=product[1]
        if stock < int(quantity):
            response=dict(
                status='Failed',
                message="Not enough {} in stock.Only {} remaining".format(product_name,product[1])
            )
            return response
        unit_price = product[2]
        price = quantity * unit_price
        try:
            sql = """INSERT INTO
                    carts  (email,product_name, quantity,price,created_at)\
                    VALUES
                    (%s,%s,%s,%s,%s)"""
            curr.execute(sql,(email,product_name,quantity,price,self.created_at))

            remaining_stock = stock - quantity
            curr.execute(
                "UPDATE products SET inventory= (%s) WHERE   product_id =(%s);",(
                    remaining_stock, product_id))
            self.db.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            response = dict(
                status="Failed.",
                Message=error
            )
            return response

        cart_item = dict(
            product_name=product_name,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            Total_price=price
        )
        response_obj = dict(
            message='cart posted successfully.',
            cart_item=cart_item,
            remaining_stock=remaining_stock

        )
        return response_obj, 201

    def get_single_cart(self,email):
        """return single cart from the db given a email"""
        # check if product exists
        if not self.check_if_cart_exists_by_email(email):
            raise NotFound(
                "No carts found for this User.")
        curr = self.db.cursor(cursor_factory=extras.DictCursor)
        curr.execute(
            "SELECT * FROM carts WHERE email = (%s);", (email,))
        rows = curr.fetchall()
        curr.close()
        resp = []

        for row in rows:
            resp.append(dict(row))

        return resp

    def check_if_cart_exists_by_email(self, email):
        database = self.db
        curr = database.cursor()
        curr.execute(
            "select * from carts where email = (%s);", (email,))
        result = curr.fetchone()
        if result:
            return True

    def get_all(self):
        """This function returns a list of all the carts"""
        dbconn = self.db
        curr = dbconn.cursor(cursor_factory=extras.DictCursor)
        curr.execute("""SELECT * FROM carts;""")
        #returns a python dictionary like interface
        rows = curr.fetchall()
        resp = []
        for row in rows:
            resp.append(dict(row))
        return resp
