import pytest
import logging
from datetime import datetime, timedelta


pytestmark = [pytest.mark.products, pytest.mark.smoke]


class TestGetProductSmoke:
    @pytest.fixture()
    def setup(self, product_setup):
        self.product_handler, self.products_db = product_setup

    @pytest.mark.tcid24
    def test_get_new_products_filter(self, setup):
        logging.info("TEST::get all products created after a certain date")

        after_date = (datetime.now().replace(microsecond=0) - timedelta(days=30)).isoformat()
        logging.info(after_date)
        products_json = self.product_handler.get_products(after=after_date)
        products_json_id = sorted([product['id'] for product in products_json])
        assert products_json, logging.warning(f"no products returned")

        # we will compare product id's from the response to the product id's in the database
        db_products = self.products_db.select_all_products(filters=f"DATE(post_date) > {after_date.split('T')[0]}")
        db_products_ids = sorted([product['ID'] for product in db_products])

        for idx, product in enumerate(products_json_id):
            assert idx < len(db_products_ids) and product == db_products_ids[idx], \
                logging.error(f"product: 'id'={product} not found in database")
