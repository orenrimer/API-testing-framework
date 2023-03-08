from src.request_handlers.customer_request import CustomerHandler
from src.db_handlers.customer_db import CustomerDB
import logging
import pytest

pytestmark = [pytest.mark.customers, pytest.mark.smoke]


class TestGetCustomerSmoke:
    @pytest.fixture()
    def setup(self):
        self.customer_handler = CustomerHandler()
        self.customer_db = CustomerDB()

    @pytest.mark.tcid12
    def test_get_existing_customer(self, setup):
        logging.info("TEST::get get existing customer")

        customer_db = self.customer_db.select_random_customer()
        if not customer_db:
            logging.warning("no customer found in database")
            return

        customer_id = customer_db[0]['ID']
        response_json = self.customer_handler.get_customer_by_id(customer_id)
        assert response_json['id'] == customer_id, logging.error(f"expected customer 'id': {customer_id} "
                                                                f"got {response_json['id']}")

    @pytest.mark.tcid13
    def test_get_non_existing_customer(self, setup):
        logging.info("TEST::get get non-existing customer")

        # get the last created customer by ID
        customer_db = self.customer_db.select_random_customer(params="order by ID desc")

        if not customer_db:
            logging.warning("No customers found in database.")
            pytest.fail()

        # incrementing the last customer ID result in a non-existing customer ID
        customer_id = customer_db[0]['ID'] + 1
        response_json = self.customer_handler.get_customer_by_id(customer_id, expected_status_code=404)
        assert 'code' in response_json and response_json['code'] == "woocommerce_rest_invalid_id",\
            logging.error(f"expected response code 'woocommerce_rest_invalid_id'")

    @pytest.mark.tcid14
    def test_get_all_customers(self, setup):
        logging.info("TEST::get all customers")

        customers = self.customer_handler.get_customers()
        customers_id = sorted([customer['id'] for customer in customers])
        customers_db_ids = sorted([customer['ID'] for customer in self.customer_db.select_all_customer()])

        for idx, customer in enumerate(customers_id):
            assert idx < len(customers_db_ids) and customer == customers_db_ids[idx], \
                logging.error(f"customer: 'id'={customer} not in database")
