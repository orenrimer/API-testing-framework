import pytest
import logging
from datetime import datetime, timedelta


pytestmark = [pytest.mark.products, pytest.mark.smoke]


class TestGetProductSmoke:
    @pytest.fixture()
    def setup(self, m_setup):
        self.request_handler, _, _, self.products_db = m_setup
        self.endpoint = "products"

    @pytest.mark.tcid24
    def test_get_filter_new_products(self, setup):
        logging.info("TEST::get all new products (posted in the last 30 days)")

        after_date = (
            datetime.now().replace(microsecond=0) - timedelta(days=30)
        ).isoformat()
        try:
            # get all products published after the given date
            products_json = self.request_handler.get_all(
                endpoint=self.endpoint, after=after_date
            )
            # get the id's of the returned products
            products_json_id = sorted([product["id"] for product in products_json])

            # get all products published after the given date from the database
            db_products = self.products_db.select_all_products(
                filters=f"DATE(post_date) > {after_date.split('T')[0]}"
            )
            # get the id's of the returned products
            db_products_ids = sorted([product["ID"] for product in db_products])

            # compare products id's
            for idx, product in enumerate(products_json_id):
                assert (
                    idx < len(db_products_ids) and product == db_products_ids[idx]
                ), logging.error(f"product: 'id'={product} not found in database")

            logging.info("SUCCESS::get all new products (posted in the last 30 days)")
        except Exception as e:
            logging.error(e)
            pytest.fail()
