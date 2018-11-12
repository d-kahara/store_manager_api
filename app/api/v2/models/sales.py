from datetime import datetime
from werkzeug.exceptions import NotFound
from ..utils.db_helper import init_db
import psycopg2.extras as extras
import psycopg2

from ..models.carts import Cart

class Sale:
    def __init__(self, **kwargs):
        """
        Sale constructor
        """
 
        self.created_at = datetime.now().replace(second=0, microsecond=0)
        self.db = init_db()

    def checkout(self, email):
        cart_items = Cart().get_single_cart(email)
        product_names = []
        products_count = 0
        cart_total = 0
        for cart in cart_items:
            product_names.append(cart['product_name'])
            products_count += cart['quantity']
            cart_total += cart['price']
        curr = self.db.cursor(cursor_factory=extras.DictCursor)
        try:
            sql = """INSERT INTO
                    sales  (email,product_names, products_count,cart_total,created_at)\
                    VALUES
                    (%s,%s,%s,%s,%s)"""
            curr.execute(sql, (email, product_names,
                               products_count, cart_total, self.created_at))

            curr.execute("DELETE FROM carts WHERE email=%s", (email,))

            self.db.commit()
            response = dict(
                status="success",
                Message='Sale Order created.'
            )
            return response

        except (Exception, psycopg2.DatabaseError) as error:
            response = dict(
                status="Failed.",
                Message=error
            )
            return response
            
    def get_all(self):
        """This function returns a list of all the sales"""
        dbconn = self.db
        curr = dbconn.cursor(cursor_factory=extras.DictCursor)
        curr.execute("""select * from sales order by created_at desc;""")
        #returns a python dictionary like interface
        rows = curr.fetchall()
        resp = []

        for row in rows:
            resp.append(dict(row))
        return resp

    def get_single_sale(self, email):
        """return single cart from the db given a email"""
        # check if product exists
        if not self.check_if_sale_exists_by_email(email):
            raise NotFound(
                "No sales found for this User.")
        curr = self.db.cursor(cursor_factory=extras.DictCursor)
        curr.execute(
            "SELECT * FROM sales WHERE email = (%s) order by created_at desc;", (email,))
        rows = curr.fetchall()
        curr.close()
        resp = []

        for row in rows:
            resp.append(dict(row))

        return resp

    def check_if_sale_exists_by_email(self, email):
        database = self.db
        curr = database.cursor()
        curr.execute(
            "select * from sales where email = (%s);", (email,))
        result = curr.fetchone()
        if result:
            return True


