import logging
import pytest

pytestmark = [pytest.mark.customers, pytest.mark.smoke]


class TestGetCustomerSmoke:
    @pytest.fixture()
    def setup(self, m_setup):
        self.request_handler, self.customer_db, _, _ = m_setup
        self.endpoint = "customers"

    @pytest.mark.tcid12
    def test_get_existing_customer(self, setup):
        logging.info("TEST::get get existing customer")

        try:
            customer_db = self.customer_db.select_random_customer()
            if not customer_db:
                raise Exception("No customers found in database.")

            customer_id = customer_db[0]['ID']
            response_json = self.request_handler.get_by_id(self.endpoint, customer_id)
            assert response_json['id'] == customer_id, logging.error(f"Invalid response. expected customer 'id': {customer_id} "
                                                                     f"got {response_json['id']}")
            logging.info("SUCCESS::get existing customer")
        except Exception as e:
            logging.error(e)
            pytest.fail()

    @pytest.mark.tcid13
    def test_get_non_existing_customer(self, setup):
        logging.info("TEST::get get non-existing customer")

        try:
            # get the last created customer by ID
            customer_db = self.customer_db.select_random_customer(params="order by ID desc")

            if not customer_db:
                raise Exception("No customers found in database.")

            # incrementing the last customer ID result in a non-existing customer ID
            customer_id = customer_db[0]['ID'] + 1
            response_json = self.request_handler.get_by_id(self.endpoint, customer_id, expected_status_code=404)
            assert 'code' in response_json and response_json['code'] == "woocommerce_rest_invalid_id", \
                logging.error(f"Invalid response, expected response code 'woocommerce_rest_invalid_id'")

            logging.info("SUCCESS::get get non-existing customer")
        except Exception as e:
            logging.error(e)
            pytest.fail()

    @pytest.mark.tcid14
    def test_get_all_customers(self, setup):
        logging.info("TEST::get all customers")

        try:
            response_json = self.request_handler.get_all(self.endpoint)

            # get the id's of the returned customers
            customers_id = sorted([customer['id'] for customer in response_json])

            # get all customers from database
            customers_db = self.customer_db.select_all_customer()
            # get the id's of the returned customers
            customers_db_ids = sorted([customer['ID'] for customer in customers_db])

            # compare customers id's
            for idx, customer in enumerate(customers_id):
                assert idx < len(customers_db_ids) and customer == customers_db_ids[idx], \
                    logging.error(f"Invalid data, customer: 'id'={customer} not in database")

            logging.info("SUCCESS::get all customers")
        except Exception as e:
            logging.error(e)
            pytest.fail()
