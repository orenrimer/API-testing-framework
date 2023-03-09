import json
import requests
from requests_oauthlib import OAuth1
from config import HOST_CONFIG
from src.utils.credentialUtils import CredentialUtils


class RequestUtils:
    def __init__(self):
        self.base_url = HOST_CONFIG['local']
        self.auth = OAuth1(client_key=CredentialUtils.get_wc_api_credentials()['key'],
                           client_secret=CredentialUtils.get_wc_api_credentials()['secret'])

    @staticmethod
    def validate_status_code(status_code, expected_status_code, url, response_json):
        assert status_code == expected_status_code, f"expected status {expected_status_code}, got {status_code}." \
                                                    f"URL: {url}, response: {response_json}"

    def get(self, endpoint, payload=None, expected_status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url=url, data=json.dumps(payload), headers={'Content-Type': 'application/json'}, auth=self.auth)
        status_code = response.status_code
        response_json = response.json()
        self.validate_status_code(status_code, expected_status_code, url, response_json)
        return response_json

    def post(self, endpoint, payload=None, expected_status_code=201):
        url = self.base_url + endpoint
        response = requests.post(url=url, data=json.dumps(payload), headers={'Content-Type': 'application/json'}, auth=self.auth)
        status_code = response.status_code
        response_json = response.json()
        self.validate_status_code(status_code, expected_status_code, url, response_json)
        return response_json

    def put(self, endpoint, payload=None, expected_status_code=200):
        url = self.base_url + endpoint
        response = requests.put(url=url, data=json.dumps(payload), headers={'Content-Type': 'application/json'}, auth=self.auth)
        status_code = response.status_code
        response_json = response.json()
        self.validate_status_code(status_code, expected_status_code, url, response_json)
        return response_json

    def delete(self, endpoint, payload=None, expected_status_code=200):
        url = self.base_url + endpoint
        response = requests.delete(url=url, data=json.dumps(payload), headers={'Content-Type': 'application/json'}, auth=self.auth)
        status_code = response.status_code
        response_json = response.json()
        self.validate_status_code(status_code, expected_status_code, url, response_json)
        return response_json
