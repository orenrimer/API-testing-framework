import os
import config
import pytest
from src.db_handlers.customer_db import CustomerDB
from src.db_handlers.order_db import OrderDB
from src.db_handlers.product_db import ProductDB
from src.request_handlers.customer_request import CustomerHandler
from src.request_handlers.order_request import OrderHandler
from src.request_handlers.product_request import ProductHandler


@pytest.fixture(scope="session")
def credentials_setup():
    os.system(f"{os.path.join(config.PATH_CONFIG['ROOT'], 'env.bat')}")


@pytest.fixture(scope="session")
def customer_setup(credentials_setup):
    customer_handler = CustomerHandler()
    customer_db = CustomerDB()
    yield customer_handler, customer_db


@pytest.fixture(scope="session")
def order_setup(credentials_setup):
    order_handler = OrderHandler()
    order_db = OrderDB()
    yield order_handler, order_db


@pytest.fixture(scope="session")
def product_setup(credentials_setup):
    product_handler = ProductHandler()
    product_db = ProductDB()
    yield product_handler, product_db
