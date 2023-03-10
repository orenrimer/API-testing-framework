from src.utils.genericUtils import generate_random_email
from src.utils.requestUtils import RequestUtils


class CustomerHandler:
    def __init__(self, base_url):
        self.requests = RequestUtils(base_url)

    def create_customer(self, payload=None, expected_status_code=201):
        email = generate_random_email()

        if payload:
            if not isinstance(payload, dict):
                raise TypeError('Invalid payload, can not create customer.')
            if "email" not in payload:
                payload["email"] = email
        else:
            # we must pass an email when creating a new customer
            payload = {"email": email}
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
