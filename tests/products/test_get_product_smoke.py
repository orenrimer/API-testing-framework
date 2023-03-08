import pytest
import logging
from datetime import datetime, timedelta
from src.db_handlers.product_db import ProductDB
from src.request_handlers.product_request import ProductHandler

pytestmark = [pytest.mark.products, pytest.mark.smoke]


class TestGetProductSmoke:
    @classmethod
    def setup(cls):
        cls.product_handler = ProductHandler()
        cls.products_db = ProductDB()

    @pytest.mark.tcid24
    def test_get_new_products_filter(self):
        logging.info("TEST::get all products created after a certain date")

        after_date = (datetime.now().replace(microsecond=0) - timedelta(days=30)).isoformat()
        logging.info(after_date)
        products_json = self.product_handler.get_products(after=after_date)
        products_json_id = sorted([product['id'] for product in products_json])
        assert products_json, logging.warning(f"no products returned")

        logging.info(products_json_id)

        db_products = self.products_db.select_all_products(filters=f"DATE(post_date) > {after_date.split('T')[0]}")
        db_products_ids = sorted([product['ID'] for product in db_products])
        logging.info(db_products_ids)

        for idx, product in enumerate(products_json_id):
            assert idx < len(db_products_ids) and product == db_products_ids[idx], \
                logging.error(f"product: 'id'={product} not found in database")
