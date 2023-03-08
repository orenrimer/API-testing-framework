import random

import pytest
import logging
from src.db_handlers.product_db import ProductDB
from src.request_handlers.product_request import ProductHandler

pytestmark = [pytest.mark.products, pytest.mark.smoke]


class TestUpdateProductSmoke:
    @classmethod
    def setup(cls):
        cls.product_handler = ProductHandler()
        cls.product_db = ProductDB()

    @pytest.mark.tcid25
    def test_update_product_price(self):
        logging.info("TEST::update product price")

        # create a test product
        product_json = self.product_handler.create_product()

        # asert response
        assert product_json['price'] == ""
        new_product_id = product_json['id']

        # update the product price
        expected_price = random.randint(0, 150)
        logging.info(expected_price)
        product_json = self.product_handler.update_product(product_id=new_product_id, payload={'regular_price': str(expected_price)})
        # assert price updated in response
        assert int(product_json['price']) == expected_price, \
            logging.error(f"Invalid price, expected {expected_price}, got { int(product_json['price'])}")

        # assert price updated in database
        product_db = self.product_db.select_product_by_id(new_product_id)
        assert int(product_db[0]['min_price']) == expected_price, \
            logging.error(f"Invalid price, expected {expected_price}, got {int(product_db[0]['min_price'])}")

        # delete test product
        self.product_handler.delete_product(new_product_id)
        assert not self.product_db.select_product_by_id(new_product_id)
