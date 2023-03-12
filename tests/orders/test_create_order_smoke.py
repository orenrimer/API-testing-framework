import logging
import random
from os import path
import pytest
from settings import DIRS
from src.utils.genericUtils import read_data_from_json, generate_random_email

pytestmark = [pytest.mark.orders, pytest.mark.smoke]


class TestCreateOrdersSmoke:
    @pytest.fixture()
    def setup(self, m_setup):
        self.request_handler, self.customer_db, self.order_db, self.product_db = m_setup

    @pytest.mark.tcid15
    def test_create_order_as_guest(self, setup):
        logging.info("TEST::create an order with a guest account")

        response_json = None
        try:
            # load test data from file
            file_path = path.join(DIRS['TEST_DATA'], "create_order_payload.json")
            payload = read_data_from_json(file_path)

            # add random items to the order payload
            random_products = self.product_db.select_random_product()
            items = [{'product_id': product['ID'], 'quantity': random.randint(1, 10)} for product in random_products]
            payload.update({"line_items": items})

            response_json = self.request_handler.create(endpoint="orders", payload=payload)
            # verify order and products
            self.verify_order_created(response_json['id'], items)
            logging.info("SUCCESS::create an order with a guest account")
        except Exception as e:
            logging.error(e)
            pytest.fail()
        finally:
            # delete the test order
            if response_json:
                self.request_handler.delete("orders", response_json['id'])

    @pytest.mark.tcid16
    def test_create_order_with_new_user(self, setup):
        logging.info("TEST::create an order with a new user account")

        customer_json = None
        order_json = None

        try:
            # add random items to the order payload
            random_products = self.product_db.select_random_product(2)
            items = [{'product_id': product['ID'], 'quantity': random.randint(1, 10)} for product in random_products]

            # create a new test customer for the order
            customer_json = self.request_handler.create(endpoint="customers",
                                                        payload={'email': generate_random_email()})
            assert customer_json
            order_json = self.request_handler.create(endpoint="orders",
                                                     payload={"line_items": items, 'customer_id': customer_json['id']})
            assert order_json['customer_id'] == customer_json['id']
            self.verify_order_created(order_json['id'], items)
            logging.info("SUCCESS::create an order with a new user account")
        except Exception as e:
            logging.error(e)
            pytest.fail()
        finally:
            # delete the test order and the test customer (if created)
            if customer_json:
                self.request_handler.delete("customers", customer_json['id'])
            if order_json:
                self.request_handler.delete("orders", order_json['id'])

    def verify_order_created(self, order_id, expected_products):
        # assert order stored in database
        assert self.order_db.select_order_by_order_id(order_id), logging.error(
            f"order: 'id'={order_id} not in database")

        # assert items
        db_order_products = self.order_db.select_order_products_by_order_id(order_id)

        tmp = {}
        for products in expected_products:
            tmp[int(products['product_id'])] = int(products['quantity'])

        for itemId in tmp:
            assert itemId in db_order_products and tmp[itemId] == db_order_products[itemId]
