from datetime import datetime
from ....data import Data


class Sales():
    """This class defines the Sales Model and
        the various its methods"""

    def __init__(self, posted_by, cart_id, cart_total, sale_id=1):
        """Initialize the Sales Model with constructor"""

        self.sale_id = len(Data.sales) + 1
        self.cart_id = cart_id
        self.posted_by = posted_by
        self.cart_total = cart_total
        self.date_created = datetime.now()
        self.date_modified = datetime.now()

    def post_sale(self):
        """Sale method to make a sale record"""

        sale = dict(
            sale_id=self.sale_id,
            cart_id=self.cart_id,
            posted_by=self.posted_by,
            cart_total=self.cart_total,
            date_created=self.date_created,
            date_modified=self.date_modified
        )
        #Save the sale to the sales List
        Data.sales.append(sale)
        return sale

    def get_all_sales(self):
        """Sale method to get all sales"""
        return Data.sales

    @staticmethod
    def get_single_sale(sale_id):
        """Sale method to get a single sale"""
        sales = Data.sales
        sale_record = [
            sale for sale in sales if int(sale['sale_id']) == int(sale_id)]
        if sale_record:
            return sale_record
        return 'not found'
