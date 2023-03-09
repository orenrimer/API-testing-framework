from src.utils.requestUtils import RequestUtils
from src.utils.genericUtils import generate_random_string


class ProductHandler:
    def __init__(self):
        self.requests = RequestUtils()

    def create_product(self, payload=None):
        name = generate_random_string(prefix='product')

        if payload:
            if not isinstance(payload, dict):
                raise TypeError('Invalid payload, can not create product.')
            if "name" not in payload:
                payload["name"] = name
        else:
            # we must pass a product name when creating a new product
            payload = {"name": name}
        product_json = self.requests.post(endpoint='products', payload=payload)
        return product_json

    def get_product_by_id(self, product_id):
        product_json = self.requests.get(endpoint=f"products/{product_id}")
        return product_json

    def get_products(self, **kwargs):
        payload = dict(kwargs)
        if 'per_page' not in payload.keys():
            payload["per_page"] = 100

        all_products = []
        max_pages = 1000
        for i in range(1, max_pages + 1):
            payload['page'] = i
            products_json = self.requests.get(endpoint='products', payload=payload)

            if not products_json:
                break
            all_products.extend(products_json)
        return all_products

    def update_product(self, product_id, payload=None, expected_status_code=200):
        if payload and not isinstance(payload, dict):
            raise Exception('Invalid payload')
        return self.requests.put(endpoint=f'products/{product_id}',
                                 expected_status_code=expected_status_code, payload=payload)

    def delete_product(self, product_id, expected_status_code=200):
        return self.requests.delete(endpoint=f'products/{product_id}',
                                    expected_status_code=expected_status_code, payload={'force': 'true'})
