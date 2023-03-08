import pytest
from src.db_handlers.order_db import OrderDB
from src.request_handlers.order_request import OrderHandler
import logging

pytestmark = [pytest.mark.orders, pytest.mark.regression]


class TestUpdateOrderSmoke:
    @pytest.fixture()
    def setup(self):
        self.order_handler = OrderHandler()
        self.order_db = OrderDB()

    @pytest.mark.parametrize("new_status",
                             [pytest.param('pending', marks=pytest.mark.tcid17),
                              pytest.param('failed', marks=pytest.mark.tcid18),
                              pytest.param('cancelled', marks=pytest.mark.tcid19),
                              pytest.param('refunded', marks=pytest.mark.tcid20),
                              pytest.param('completed', marks=pytest.mark.tcid21),
                              pytest.param('on-hold', marks=pytest.mark.tcid22),
                              ])
    def test_update_order_status(self, setup, new_status):
        # create new order
        order_json = self.order_handler.create_order()
        order_id = order_json['id']
        logging.info(order_id)
        new_status = new_status

        # get the curr order status
        assert order_json['status'] == 'pending'

        # update the status
        self.order_handler.update_order(order_id=order_id, payload={'status': new_status})

        # retrieve the order info one more time
        db_status = self.order_db.select_order_status(order_id)
        logging.info(db_status)

        # verify the order status in db
        assert db_status['status'] == new_status, f"failed to update order's status. expected status {new_status}, " \
                                                  f"got {db_status['status']}"
