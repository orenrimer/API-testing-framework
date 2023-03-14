from src.utils.dbUtils import DbUtils
import random


class ProductDB:
    def __init__(self, host, port, db_name):
        self.db = DbUtils(host, port, db_name)
        self.POSTS_TABLE_NAME = f"{db_name}.wp_posts"
        self.POSTS_META_TABLE_NAME = f"{db_name}.wp_wc_product_meta_lookup"

    def select_product_by_id(self, product_id):
        """
        select a product from the db using a given product id
        """
        return self.db.select(
            [self.POSTS_TABLE_NAME, self.POSTS_META_TABLE_NAME],
            where=f"{self.POSTS_TABLE_NAME}.ID = {self.POSTS_META_TABLE_NAME}.product_id and post_type='product' and ID={product_id}",
        )

    def select_random_product(self, qty=1):
        """
        select a random product(s) from the db
        """
        products = self.db.select(
            [self.POSTS_TABLE_NAME], where="post_type='product'", limit=qty
        )
        return random.sample(products, k=qty)

    def select_all_products(self, filters=None):
        """
        select all products from the db
        """
        return self.db.select(
            [self.POSTS_TABLE_NAME],
            where=f"post_type='product' {'and ' + filters if filters else ''}",
        )
