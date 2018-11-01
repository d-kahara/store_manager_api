from datetime import datetime
from werkzeug.exceptions import NotFound
from ..utils.db_helper import init_db
from flask import request
import psycopg2.extras as extras



class Sale:
    def __init__(self, product_id=0, quantity=0, attendant_id=0):
        """
        sale constructor
        # """
        self.product_id = product_id
        self.quantity = quantity
        self.attendant_id = attendant_id
        self.created_at = datetime.now().replace(second=0, microsecond=0)
        self.db = init_db()


    def make_sale(self, product_id, quantity, attendant_id):
          
        curr = self.db.cursor()
        curr.execute(
            "select * from products where product_id = (%s);", (product_id,))
        product = curr.fetchone()
        print(product)
        if  not product:
            raise NotFound('Product does not exist.')
        product_name = product[7].lower()
        stock=product[1]
        if stock < int(quantity):
            # print('Out of stock.')
            response=dict(
                status='Failed',
                message="Not enough {} in stock.Only {} remaining".format(product_name,product[1])
            )
            return response

        price = quantity * product[2]
        print(price)
        

        new_sale = dict(
            product_name=product_name,
            attendant_id=attendant_id,
            quantity=quantity,
            price=price,
            created_at=self.created_at
        )
        item = """INSERT INTO
                sales  (attendant_id,product_name, quantity,price,created_at)
                VALUES
                (%(attendant_id)s,%(product_name)s,%(quantity)s,%(price)s,%(created_at)s)"""
        curr.execute(item, new_sale)

        remaining_stock = stock - quantity
        curr.execute(
            "UPDATE products SET inventory= (%s) WHERE   product_id =(%s);",(
                remaining_stock, product_id))
        self.db.commit()

        sold_item = dict(
            product_name=product_name,
            product_id=product_id,
            quantity=quantity,
            Total_price=price
        )
        response_obj = dict(
            message='Sale made successfully.',
            sold_item=sold_item,
            remaining_stock=remaining_stock

        )
        return response_obj, 201

    def get_single_sale(self, sale_id):
        """return single sale from the db given a sale_id"""
        # check if product exists
        if not self.check_if_product_exists_by_id(sale_id):
            raise NotFound(
                "Sale  does not exist.")
        curr = self.db.cursor(cursor_factory=extras.DictCursor)
        curr.execute(
            "SELECT * FROM sales WHERE sale_id = (%s);", (sale_id,))
        rows = curr.fetchall()
        curr.close()
        resp = []

        for row in rows:
            resp.append(dict(row))
            # print(row)
        print(resp)

        return resp

    def check_if_product_exists_by_id(self, sale_id):
        database = self.db
        curr = database.cursor()
        curr.execute(
            "select * from sales where sale_id = (%s);", (sale_id,))
        result = curr.fetchone()
        print(result)
        if result:
            return True

    def get_all(self):
        """This function returns a list of all the sales"""
        dbconn = self.db
        curr = dbconn.cursor(cursor_factory=extras.DictCursor)
        curr.execute("""SELECT * FROM sales;""")
        #returns a python dictionary like interface
        rows = curr.fetchall()
        resp = []
        for row in rows:
            resp.append(dict(row))
        return resp
