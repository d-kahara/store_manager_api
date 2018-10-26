from datetime import datetime
from ..utils.db_helper import init_db
import psycopg2.extras as extras


class Sales():
    """This class defines the Sales Model and
        the various its methods"""

    def __init__(self, posted_by, cart, cart_total):
        """Initialize the Sales Model with constructor"""

 
        self.cart = cart
        self.posted_by = posted_by
        self.date_created = datetime.now()
        self.date_modified = datetime.now()
        self.db = init_db()

    def post_sale(self):
        """Sale method to make a sale record"""

        new_sale = dict(
            cart=[],
            posted_by=self.posted_by,
            cart_total=self.cart_total,
            date_created=self.date_created,
        )
        sql = """INSERT INTO sales (product_name,min_quantity, category, inventory,date_created) \
            VALUES ( %(product_name)s, %(min_quantity)s, %(category)s, %(inventory)s, %(date_created)s);
            """
        curr.execute(sql, new_sale)
        self.db.commit()
        curr.close()



    def get_all_sales(self):
        """Sale method to get all sales"""
        dbconn = self.db
        curr = dbconn.cursor(cursor_factory=extras.DictCursor)
        curr.execute("""SELECT * FROM sales;""")
        #returns a python dictionary like interface
        data = curr.fetchall()
        resp = []

        for row in data:
            resp.append(dict(row))
        return resp

    @staticmethod
    def get_single_sale(sale_id):
        """Sale method to get a single sale"""
        sales = Data.sales
        sale_record = [
            sale for sale in sales if int(sale['sale_id']) == int(sale_id)]
        if sale_record:
            return sale_record
        return 'not found'

    def check_if_product_exists(self, product_name):
        database = self.db
        curr = database.cursor()
        curr.execute(
            "select * from products where product_name = (%s);", (product_name,))
        result = curr.fetchone()
        if result:
            return True
