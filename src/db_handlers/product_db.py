from src.config import DB_CONFIG
from src.utils.dbUtils import DbUtils
import random


class ProductDB:
    def __init__(self):
        self.db = DbUtils()
        self.POSTS_TABLE_NAME = f"{DB_CONFIG['localhost']['table_prefix']}posts"
        self.POSTS_META_TABLE_NAME = f"{DB_CONFIG['localhost']['table_prefix']}wc_product_meta_lookup"

    def select_product_by_name(self, name):
        #     """
        #         select a product from the db using a given product name
        #     """
        sql = f"SELECT p1.*, p2.*" \
              f"FROM {DB_CONFIG['localhost']['database']}.{self.POSTS_TABLE_NAME} AS `p1`, {DB_CONFIG['localhost']['database']}.{self.POSTS_META_TABLE_NAME} AS `p2` " \
              f"WHERE p1.ID = p2.product_id AND p1.post_type='product' AND p1.post_title={name};"
        return self.db.select(sql)

    def select_product_by_id(self, product_id):
        """
             select a product from the db using a given product id
        """
        sql = f"SELECT p1.*, p2.*" \
              f"FROM {DB_CONFIG['localhost']['database']}.{self.POSTS_TABLE_NAME} AS `p1`, {DB_CONFIG['localhost']['database']}.{self.POSTS_META_TABLE_NAME} AS `p2` " \
              f"WHERE p1.ID = p2.product_id AND p1.post_type='product' AND p1.ID={product_id};"
        return self.db.select(sql)

    def select_random_product(self, qty=1):
        """
            select a random product(s) from the db
        """
        sql = f"SELECT * FROM {DB_CONFIG['localhost']['database']}.{self.POSTS_TABLE_NAME} WHERE post_type='product' limit {qty}; "
        products = self.db.select(sql)
        return random.sample(products, k=qty)

    def select_all_products(self, filters=None):
        """
            select all products from the db
        """
        sql = f"SELECT * FROM {DB_CONFIG['localhost']['database']}.{self.POSTS_TABLE_NAME} WHERE post_type='product' " \
              f"{'and ' + filters if filters else ''};"
        return self.db.select(sql)
