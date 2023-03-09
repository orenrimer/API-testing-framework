import logging
import pytest
from src.utils.genericUtils import generate_random_email

pytestmark = [pytest.mark.customers, pytest.mark.smoke]


class TestCreateCustomerSmoke:
    @pytest.fixture()
    def setup(self, customer_setup):
        self.customer_handler,  self.customer_db = customer_setup

    @pytest.mark.tcid10
    def test_create_customer_email_and_password(self, setup):
        logging.info("TEST::create a new customer with email and password only")

        # generate random customer info
        email = generate_random_email()
        response_json = None
        try:
            response_json = self.customer_handler.create_customer(payload={'email': email})
        except TypeError:
            logging.error(TypeError)
            pytest.fail()

        # assert API response
        assert response_json['email'] == email, logging.error(f"expected email: {email}, got {response_json['email']}")
        assert response_json['first_name'] == "", logging.error("customer first name should be empty")

        # verify customer created in DB
        new_id = response_json['id']
        customer_db = self.customer_db.select_customer_by_email(response_json['email'])
        assert customer_db[0]['ID'] == new_id, logging.error(f"expected id: {new_id}, got {customer_db[0]['id']}")

        # delete test customer
        self.customer_handler.delete_customer(new_id)
        assert not self.customer_db.select_customer_by_id(new_id)

    @pytest.mark.tcid11
    def test_create_customer_with_existing_email(self, setup):
        logging.info("TEST::create a new customer with an existing email")

        customer_db = self.customer_db.select_random_customer()
        # if there are no customers in the database
        if not customer_db:
            logging.warning("no customer found in database")
            pytest.fail()

        email = customer_db[0]['user_email']
        response_json = None
        try:
            response_json = self.customer_handler.create_customer(payload={'email': email}, expected_status_code=400)
        except TypeError:
            logging.error(TypeError)
            pytest.fail()

        assert 'code' in response_json and response_json['code'] == "registration-error-email-exists", \
            logging.error(f"excepted response code: registration-error-email-exists got {response_json['code']}")
