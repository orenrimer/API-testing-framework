from src.utils.genericUtils import generate_random_email, generate_random_password
from src.utils.requestUtils import RequestUtils


class CustomerHandler:
    def __init__(self):
        self.requests = RequestUtils()

    def create_customer(self, email=None, password=None, expected_status_code=201, **kwargs):
        if not email:
            email = generate_random_email()
        if not password:
            password = generate_random_password()

        payload = {'email': email, 'password': password}
        payload.update(kwargs)

        customer_json = self.requests.post(endpoint='customers', payload=payload,
                                           expected_status_code=expected_status_code)
        return customer_json

    def get_customers(self, **kwargs):
        payload = dict(kwargs)
        if 'per_page' not in payload.keys():
            payload['per_page'] = 100

        all_customers = []
        max_pages = 1000
        for i in range(1, max_pages + 1):
            payload['page'] = i
            response_json = self.requests.get(endpoint='customers', payload=payload)

            if not response_json:
                break
            all_customers.extend(response_json)
        return all_customers

    def get_customer_by_id(self, customer_id, expected_status_code=200):
        return self.requests.get(endpoint=f'customers/{customer_id}', expected_status_code=expected_status_code)

    def delete_customer(self, customer_id, expected_status_code=200):
        return self.requests.delete(endpoint=f'customers/{customer_id}',
                                    payload={"force": "true"}, expected_status_code=expected_status_code)
