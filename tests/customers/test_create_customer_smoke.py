import logging
import pytest
from settings import DIRS
from os import path
from src.utils.genericUtils import read_data_from_json

pytestmark = [pytest.mark.customers, pytest.mark.smoke]


class TestCreateCustomerSmoke:
    @pytest.fixture()
    def setup(self, customer_setup):
        self.customer_handler, self.customer_db = customer_setup

    @pytest.mark.tcid10
    @pytest.mark.poitive
    def test_create_new_customer(self, setup):
        logging.info("TEST::create a new customer with email only")

        response_json = None
        try:
            # read test date from file
            file_path = path.join(DIRS['TEST_DATA'], "create_customer_payload.json")
            payload = read_data_from_json(file_path)
            response_json = self.customer_handler.create_customer(payload=payload)
            # assert API response
            assert response_json['email'] == payload['email'], logging.error(f"Invalid response, expected email: {payload['email']},"
                                                                             f" got {response_json['email']}")

            assert response_json['first_name'] == payload['first_name'], logging.error(
                "Invalid response, expected email: {payload['email']} got {response_json['email']}")

            # verify customer created in DB
            customer_db = self.customer_db.select_customer_by_email(response_json['email'])
            assert customer_db[0]['ID'] == response_json['id'], logging.error(
                f"Invalid data, expected id: {response_json['id']}, got {customer_db[0]['id']}")

            logging.info("SUCCESS::create a new customer with an existing email")
        except Exception as e:
            logging.error(e)
            pytest.fail()
        finally:
            # delete test customer
            if response_json:
                self.customer_handler.delete_customer(response_json['id'])

    @pytest.mark.tcid11
    @pytest.mark.negetive
    def test_create_customer_with_existing_email(self, setup):
        logging.info("TEST::create a new customer with an existing email")

        try:
            # get random customer from database
            customer_db = self.customer_db.select_random_customer()
            if not customer_db:
                raise Exception("No customer found in database")

            email = customer_db[0]['user_email']
            response_json = self.customer_handler.create_customer(payload={'email': email}, expected_status_code=400)
            # assert response
            assert 'code' in response_json and response_json['code'] == "registration-error-email-exists", \
                logging.error(f"Invalid response, "
                              f"excepted response code: registration-error-email-exists got {response_json['code']}")

            logging.info("SUCCESS::create a new customer with an existing email")
        except Exception as e:
            logging.error(e)
            pytest.fail()
