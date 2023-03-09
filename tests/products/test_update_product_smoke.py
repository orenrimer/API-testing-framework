import random
import pytest
import logging


pytestmark = [pytest.mark.products, pytest.mark.smoke]


class TestUpdateProductSmoke:
    @pytest.fixture()
    def setup(self, product_setup):
        self.product_handler, self.product_db = product_setup

    @pytest.mark.tcid25
    def test_update_product_price(self, setup):
        logging.info("TEST::update product price")

        product_json = None
        expected_price = random.randint(0, 150)

        try:
            # create a test product
            product_json = self.product_handler.create_product()
            assert product_json['price'] == ""
            # update the product price
            product_json = self.product_handler.update_product(product_id=product_json['id'], payload={'regular_price': str(expected_price)})

            # assert price updated in response
            assert int(product_json['price']) == expected_price, \
                logging.error(f"Invalid price, expected {expected_price}, got {int(product_json['price'])}")

            # assert price updated in database
            product_db = self.product_db.select_product_by_id(product_json['id'])
            assert int(product_db[0]['min_price']) == expected_price, \
                logging.error(f"Invalid price, expected {expected_price}, got {int(product_db[0]['min_price'])}")
        except Exception:
            logging.info(Exception)
            pytest.fail()
        finally:
            if product_json:
                # delete test product
                self.product_handler.delete_product(product_json['id'])
                assert not self.product_db.select_product_by_id(product_json['id'])
