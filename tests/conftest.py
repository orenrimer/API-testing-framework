from src.utils.custom_logger import set_logger_config
from src.utils.genericUtils import read_data_from_json
from src.db_handlers.customer_db import CustomerDB
from src.db_handlers.order_db import OrderDB
from src.db_handlers.product_db import ProductDB
from src.request_handler import RequestHandler
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
def m_setup(config):
    request = RequestHandler(config['HOST']['local'])
    customer_db = CustomerDB(config['DB']['local']['host'],
                             config['DB']['local']['port'],
                             config['DB']['local']['database'])

    order_db = OrderDB(config['DB']['local']['host'],
                       config['DB']['local']['port'],
                       config['DB']['local']['database'])

    product_db = ProductDB(config['DB']['local']['host'],
                           config['DB']['local']['port'],
                           config['DB']['local']['database'])
    return request, customer_db, order_db, product_db
