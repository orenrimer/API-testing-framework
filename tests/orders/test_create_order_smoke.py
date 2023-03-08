import logging
import random
import pytest
from src.db_handlers.order_db import OrderDB
from src.db_handlers.customer_db import CustomerDB
from src.db_handlers.product_db import ProductDB
from src.request_handlers.customer_request import CustomerHandler
from src.request_handlers.order_request import OrderHandler

pytestmark = [pytest.mark.orders, pytest.mark.smoke]


class TestCreateOrdersSmoke:
    @pytest.fixture()
    def setup(self):
        self.product_db = ProductDB()
        self.order_db = OrderDB()
        self.order_handler = OrderHandler()
        self.customer_handler = CustomerHandler()
        self.customer_db = CustomerDB()

    @pytest.mark.tcid15
    def test_create_order_as_guest(self, setup):
        logging.info("TEST::create an order with a guest account")

        # add random items to the order payload
        random_products = self.product_db.select_random_product(2)
        items = [{'product_id': product['ID'], 'quantity': random.randint(1, 10)} for product in random_products]
        response_json = self.order_handler.create_order(payload={"line_items": items})

        self.verify_order_created(response_json['id'], items)

        # delete the order and the new customer
        self.order_handler.delete_order(response_json['id'])
        assert not self.order_db.select_order_by_order_id(response_json['id'])

    @pytest.mark.tcid16
    def test_create_order_with_new_user(self, setup):
        logging.info("TEST::create an order with a new user account")

        # create a new customer
        new_customer_json = self.customer_handler.create_customer()
        assert new_customer_json

        new_customer_id = new_customer_json['id']

        # add random items to the order payload
        random_products = self.product_db.select_random_product(2)
        items = [{'product_id': product['ID'], 'quantity': random.randint(1, 10)} for product in random_products]
        response_json = self.order_handler.create_order(payload={"line_items": items, 'customer_id': new_customer_id})

        self.verify_order_created(response_json['id'], items)

        # delete the order and the new customer
        self.customer_handler.delete_customer(new_customer_id)
        self.order_handler.delete_order(response_json['id'])
        assert not self.customer_db.select_customer_by_id(new_customer_id) and not self.order_db.select_order_by_order_id(response_json['id'])

    def verify_order_created(self, order_id, expected_products):
        # assert order stored in database
        assert self.order_db.select_order_by_order_id(order_id), logging.error(f"order: 'id'={order_id} not in database")

        # assert items
        db_order_products = self.order_db.select_order_products_by_order_id(order_id)

        tmp = {}
        for products in expected_products:
            tmp[int(products['product_id'])] = int(products['quantity'])

        for itemId in tmp:
            assert itemId in db_order_products and tmp[itemId] == db_order_products[itemId], \
                logging.error(f"product: 'id'={itemId} not found in order")
