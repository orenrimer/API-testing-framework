import pytest
import logging

pytestmark = [pytest.mark.orders, pytest.mark.regression]


class TestUpdateOrderSmoke:
    @pytest.fixture()
    def setup(self, customer_setup):
        self.order_handler, self.order_db = customer_setup

    @pytest.mark.parametrize("new_status",
                             [pytest.param('pending', marks=pytest.mark.tcid17),
                              pytest.param('failed', marks=pytest.mark.tcid18),
                              pytest.param('cancelled', marks=pytest.mark.tcid19),
                              pytest.param('refunded', marks=pytest.mark.tcid20),
                              pytest.param('completed', marks=pytest.mark.tcid21),
                              pytest.param('on-hold', marks=pytest.mark.tcid22),
                              ])
    def test_update_order_status(self, setup, new_status):
        new_status = new_status
        order_json = None

        try:
            # create new order
            order_json = self.order_handler.create_order()
            assert order_json['status'] == 'pending'
            # update the status
            self.order_handler.update_order(order_id=order_json['id'], payload={'status': new_status})
            # check status changed in database
            db_status = self.order_db.select_order_status(order_json['id'])
            assert db_status['status'] == new_status, f"failed to update order's status. expected status {new_status}, " \
                                                      f"got {db_status['status']}"
        except Exception:
            logging.error(Exception)
            pytest.fail()
        finally:
            if order_json:
                self.order_handler.delete_order(order_json['id'])
                assert not self.order_db.select_order_by_order_id(order_json['id'])
