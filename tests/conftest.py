import logging
from src.utils.credentialUtils import CredentialUtils
from src.utils.custom_logger import set_logger_config
from src.utils.genericUtils import read_data_from_json
from src.db_handlers.customer_db import CustomerDB
from src.db_handlers.order_db import OrderDB
from src.db_handlers.product_db import ProductDB
from src.request_handlers.customer_request import CustomerHandler
from src.request_handlers.order_request import OrderHandler
from src.request_handlers.product_request import ProductHandler
from settings import DIRS
from dotenv import load_dotenv
from os.path import join
import pytest


@pytest.fixture(scope="session")
def config():
    # load api keys
    load_dotenv()

    # read config file
    config_path = join(DIRS['TEST'], "properties", "test_config.json")
    data = read_data_from_json(config_path)

    # add logger configuration
    set_logger_config()
    return data


@pytest.fixture(scope="session")
def customer_setup(config):
    customer_handler = CustomerHandler(config['HOST']['local'])
    customer_db = CustomerDB(config['DB']['local']['host'],
                             config['DB']['local']['port'],
                             config['DB']['local']['database'])
    yield customer_handler, customer_db


@pytest.fixture(scope="session")
def order_setup(config):
    order_handler = OrderHandler(config['HOST']['local'])
    order_db = OrderDB(config['DB']['local']['host'],
                       config['DB']['local']['port'],
                       config['DB']['local']['database'])
    yield order_handler, order_db


@pytest.fixture(scope="session")
def product_setup(config):
    product_handler = ProductHandler(config['HOST']['local'])
    product_db = ProductDB(config['DB']['local']['host'],
                           config['DB']['local']['port'],
                           config['DB']['local']['database'])
    yield product_handler, product_db
