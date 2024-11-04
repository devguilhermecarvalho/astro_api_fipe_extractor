import requests
import time

class BaseConnector:
    def __init__(self, url, headers=None, max_retries=3, delay=1.5):
        self.url = url
        self.headers = headers or {}
        self.max_retries = max_retries
        self.delay = delay

    def post(self, data=None):
        retries = 0
        while retries < self.max_retries:
            try:
                response = requests.post(self.url, json=data, headers=self.headers)
                if response.status_code == 200:
                    return response.json()
                else:
                    return None
            except requests.exceptions.RequestException:
                retries += 1
                time.sleep(self.delay * retries)
        return None
