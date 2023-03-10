from src.utils.dbUtils import DbUtils


class OrderDB:
    def __init__(self, host, port, db_name):
        self.db = DbUtils(host, port, db_name)
        self.ORDER_TABLE_NAME = f"{db_name}.wp_woocommerce_order_items"
        self.ORDER_ITEMS_TABLE_NAME = f"{db_name}.wp_woocommerce_order_itemmeta"
        self.ORDER_STATS_TABLE_NAME = f"{db_name}.wp_wc_order_stats"

    def select_order_by_order_id(self, order_id):
        """
            select an order from the db using a given order id
        """
        sql = f"SELECT * FROM {self.ORDER_TABLE_NAME} WHERE order_id={order_id};"
        return self.db.select(sql)

    def select_order_status(self, order_id):
        """
            select an order from the db using a given customer id
        """
        sql = f"SELECT * FROM {self.ORDER_STATS_TABLE_NAME} WHERE order_id={order_id};"
        return self.db.select(sql)

    def select_order_products_by_order_id(self, order_id):
        """
            select all the products that have been purchased in a given order
        """
        sql = f"SELECT * " \
              f"FROM {self.ORDER_TABLE_NAME} natural join {self.ORDER_ITEMS_TABLE_NAME} " \
              f"WHERE order_id={order_id} and order_item_type='line_item';"
        data = self.db.select(sql)

        items = {}
        for d in data:
            if d['order_item_id'] not in items:
                items[d['order_item_id']] = {}

            if d['meta_key'] == "_product_id":
                items[d['order_item_id']].update({"id": d['meta_value']})
            elif d['meta_key'] == "_qty":
                items[d['order_item_id']].update({"quantity": d['meta_value']})

        res = {}
        for item in items.values():
            res[int(item['id'])] = int(item['quantity'])
        return res
