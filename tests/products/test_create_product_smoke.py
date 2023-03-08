import logging
import pytest
from src.db_handlers.product_db import ProductDB
from src.request_handlers.product_request import ProductHandler
from src.utils.genericUtils import generate_random_string

pytestmark = [pytest.mark.products, pytest.mark.smoke]


class TestCreateProduct:
    @pytest.fixture()
    def setup(self):
        self.product_handler = ProductHandler()
        self.product_db = ProductDB()

    @pytest.mark.tcid23
    def test_create_product_name_only(self, setup):
        logging.info("TEST::create a new product with name only")
        name = generate_random_string(prefix="product")

        # create a new product
        product_json = self.product_handler.create_product(name=name)

        # asert response
        assert product_json['name'] == name, logging.error(f"expected name: {name}, got {product_json['name']}")

        # assert product created
        new_product_id = product_json['id']
        product_db = self.product_db.select_product_by_id(new_product_id)

        assert product_db[0]['post_title'] == name, \
            logging.error(f"expected name: {name}, got {product_db[0]['post_title']}")

        # delete test product
        self.product_handler.delete_product(new_product_id)
        assert not self.product_db.select_product_by_id(new_product_id)
