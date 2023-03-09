import logging
import pytest
from src.utils.genericUtils import read_data_from_json

pytestmark = [pytest.mark.products, pytest.mark.smoke]


class TestCreateProduct:
    @pytest.fixture()
    def setup(self, product_setup):
        self.product_handler, self.product_db = product_setup

    @pytest.mark.tcid23
    def test_create_product(self, setup):
        logging.info("TEST::create a new product")

        # create a new product
        payload = read_data_from_json('create_product_payload.json')
        product_json = None

        try:
            product_json = self.product_handler.create_product(payload=payload)
        except Exception:
            logging.error(Exception)
            pytest.fail()

        # asert response
        assert product_json['name'] == payload['name'], logging.error(f"expected name: {payload['name']}, "
                                                                      f"got {product_json['name']}")
        assert product_json['price'] == payload['regular_price'], \
            logging.error(f"expected price: {payload['regular_price']}, got {product_json['price']}")

        # assert product created in db
        new_product_id = product_json['id']
        product_db = self.product_db.select_product_by_id(new_product_id)

        assert product_db[0]['post_title'] == payload['name'], \
            logging.error(f"expected name: {payload['name']}, got {product_db[0]['post_title']}")

        # delete test product
        self.product_handler.delete_product(new_product_id)
        assert not self.product_db.select_product_by_id(new_product_id)
