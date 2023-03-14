import logging
from os import path

import pytest

from settings import DIRS
from src.utils.genericUtils import read_data_from_json

pytestmark = [pytest.mark.products, pytest.mark.smoke]


class TestCreateProduct:
    @pytest.fixture()
    def setup(self, m_setup):
        self.request_handler, _, _, self.product_db = m_setup
        self.endpoint = "products"

    @pytest.mark.tcid23
    def test_create_product(self, setup):
        logging.info("TEST::create a new product")

        product_json = None
        try:
            # read test data from file
            file_path = path.join(DIRS["TEST_DATA"], "create_product_payload.json")
            payload = read_data_from_json(file_path)

            # create test product
            product_json = self.request_handler.create(
                endpoint=self.endpoint, payload=payload
            )

            # asert response
            assert product_json["name"] == payload["name"], logging.error(
                f"expected name: {payload['name']}, " f"got {product_json['name']}"
            )
            assert product_json["price"] == payload["regular_price"], logging.error(
                f"expected price: {payload['regular_price']}, got {product_json['price']}"
            )

            # assert product created in db
            product_db = self.product_db.select_product_by_id(product_json["id"])
            assert product_db[0]["post_title"] == payload["name"], logging.error(
                f"expected name: {payload['name']}, got {product_db[0]['post_title']}"
            )

            logging.info("SUCCESS::create a new product")
        except Exception as e:
            logging.error(e)
            pytest.fail()
        finally:
            # delete test product
            self.request_handler.delete(self.endpoint, product_json["id"])
