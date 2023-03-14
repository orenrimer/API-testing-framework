from src.utils.requestUtils import RequestUtils


class RequestHandler:
    def __init__(self, base_url):
        self.requests = RequestUtils(base_url)

    def create(self, endpoint, payload=None, expected_status_code=201):
        if payload:
            if not isinstance(payload, dict):
                raise TypeError("Invalid payload, can not send request.")
        response = self.requests.post(endpoint=endpoint, payload=payload)
        response_json = response.json()
        self.validate_status_code(
            response.status_code, expected_status_code, response_json
        )
        return response_json

    def get_all(self, endpoint, expected_status_code=200, **kwargs):
        payload = dict(kwargs)
        if "per_page" not in payload.keys():
            payload["per_page"] = 100

        all_customers = []
        max_pages = 1000
        for i in range(1, max_pages + 1):
            payload["page"] = i
            response = self.requests.get(endpoint=endpoint, payload=payload)
            response_json = response.json()
            self.validate_status_code(
                response.status_code, expected_status_code, response_json
            )
            if not response_json:
                break
            all_customers.extend(response_json)
        return all_customers

    def get_by_id(self, endpoint, id, expected_status_code=200):
        response = self.requests.get(endpoint=f"{endpoint}/{id}")
        response_json = response.json()
        self.validate_status_code(
            response.status_code, expected_status_code, response_json
        )
        return response_json

    def update(self, endpoint, id, payload=None, expected_status_code=200):
        if payload and not isinstance(payload, dict):
            raise Exception("Invalid payload")
        response = self.requests.put(endpoint=f"{endpoint}/{id}", payload=payload)
        response_json = response.json()
        self.validate_status_code(
            response.status_code, expected_status_code, response_json
        )
        return response_json

    def delete(self, endpoint, id, expected_status_code=200):
        response = self.requests.delete(
            endpoint=f"{endpoint}/{id}", payload={"force": "true"}
        )
        response_json = response.json()
        self.validate_status_code(
            response.status_code, expected_status_code, response_json
        )
        return response_json

    @staticmethod
    def validate_status_code(status_code, expected_status_code, response_json):
        if status_code != expected_status_code:
            raise Exception(
                f"Invalid response. expected status {expected_status_code}, "
                f"got {status_code}.\nresponse body: {response_json}"
            )
