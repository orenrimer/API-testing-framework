import random
import pytest
import logging

pytestmark = [pytest.mark.products, pytest.mark.smoke]


class TestUpdateProductSmoke:
    @pytest.fixture()
    def setup(self, m_setup):
        self.request_handler, _, _, self.product_db = m_setup
        self.endpoint = "products"

    @pytest.mark.tcid25
    def test_update_product_price(self, setup):
        logging.info("TEST::update product price")

        new_price = random.randint(0, 150)
        product_json = None

        try:
            # create a test product
            product_json = self.request_handler.create(self.endpoint)
            assert product_json["price"] == ""

            # update the product price
            product_json = self.request_handler.update(
                self.endpoint,
                product_json["id"],
                payload={"regular_price": str(new_price)},
            )

            # assert price updated in response
            assert int(product_json["price"]) == new_price, logging.error(
                f"Invalid price, expected {new_price},"
                f" got {int(product_json['price'])}"
            )

            # assert price updated in database
            product_db = self.product_db.select_product_by_id(product_json["id"])
            assert int(product_db[0]["min_price"]) == new_price, logging.error(
                f"Invalid price, expected {new_price}, "
                f"got {int(product_db[0]['min_price'])}"
            )

            logging.info("SUCCESS::update product price")
        except Exception as e:
            logging.error(e)
            pytest.fail()
        finally:
            if product_json:
                # delete test product
                self.request_handler.delete(self.endpoint, product_json["id"])
