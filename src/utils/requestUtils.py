import json
import requests
from requests_oauthlib import OAuth1
from src.utils.credentialUtils import CredentialUtils


class RequestUtils:
    def __init__(self, base_url):
        self.base_url = base_url
        self.auth = OAuth1(client_key=CredentialUtils.get_wc_api_credentials()['key'],
                           client_secret=CredentialUtils.get_wc_api_credentials()['secret'])

    def get(self, endpoint, payload=None):
        url = self.base_url + endpoint
        response = requests.get(url=url, data=json.dumps(payload),
                                headers={'Content-Type': 'application/json'}, auth=self.auth)
        return response

    def post(self, endpoint, payload=None):
        url = self.base_url + endpoint
        response = requests.post(url=url, data=json.dumps(payload),
                                 headers={'Content-Type': 'application/json'}, auth=self.auth)
        return response

    def put(self, endpoint, payload=None):
        url = self.base_url + endpoint
        response = requests.put(url=url, data=json.dumps(payload),
                                headers={'Content-Type': 'application/json'}, auth=self.auth)
        return response

    def delete(self, endpoint, payload=None):
        url = self.base_url + endpoint
        response = requests.delete(url=url, data=json.dumps(payload),
                                   headers={'Content-Type': 'application/json'}, auth=self.auth)
        return response
