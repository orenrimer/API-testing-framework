from src.utils.requestUtils import RequestUtils


class OrderHandler:
    def __init__(self):
        self.requests = RequestUtils()

    def get_order_by_id(self, order_id, expected_status_code=200):
        return self.requests.get(endpoint=f"orders/{order_id}", expected_status_code=expected_status_code)

    def get_orders(self, **kwargs):
        payload = dict(kwargs)
        if 'per_page' not in payload.keys():
            payload['per_page'] = 100

        all_products = []
        max_pages = 1000
        for i in range(1, max_pages + 1):
            payload['page'] = i
            response = self.requests.get(endpoint='products', payload=payload)

            if not response:
                break
            all_products.extend(response)
        return all_products

    def create_order(self, payload=None, expected_status_code=201):
        if payload:
            assert isinstance(payload, dict)
        return self.requests.post(endpoint='orders', payload=payload, expected_status_code=expected_status_code)

    def update_order(self, order_id, payload=None, expected_status_code=200):
        if payload:
            assert isinstance(payload, dict)
        return self.requests.put(endpoint=f'orders/{order_id}', payload=payload,
                                 expected_status_code=expected_status_code)

    def delete_order(self, order_id, expected_status_code=200):
        return self.requests.delete(endpoint=f'orders/{order_id}', payload={"force": "true"},
                                    expected_status_code=expected_status_code)
