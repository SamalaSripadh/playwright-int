import requests


class BaseClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def request(self, method, endpoint, **kwargs):
        return self.session.request(
            method,
            f"{self.base_url}{endpoint}",
            timeout=30,
            **kwargs,
        )