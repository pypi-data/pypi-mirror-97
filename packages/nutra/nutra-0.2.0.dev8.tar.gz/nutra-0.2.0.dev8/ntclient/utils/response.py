from datetime import datetime

import requests


class Response:
    def __init__(self, url, auth_token=None):
        self.url = url
        self.initial_time = datetime.now()
        self.auth_token = auth_token
        self.headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else None

    def build_response(self):
        self.code = self.Response.status_code  # or self.res["code"]

        # TODO: try/catch if server returns XML/HTML error, .json() will fail..
        self.res = self.Response.json()
        self.data = self.res["data"]
        self.ok = self.res["status"] == "OK"
        if not self.ok:
            self.error = self.data["error"]

        self.program = self.res["program"]
        self.version = self.res["version"]
        self.release = self.res["release"]

        self.server_datetime = datetime.fromtimestamp(self.res["timestamp"])
        self.final_time = datetime.now()
        self.delay = round((self.final_time - self.initial_time).total_seconds() * 1000)

    #
    # HTTP Methods
    def get(self, params=None):
        self.params = params
        self.Response = requests.get(self.url, params=params, headers=self.headers)
        self.build_response()

    def delete(self):
        self.Response = requests.delete(self.url, headers=self.headers)
        self.build_response()

    def post(self, body=None):
        self.body = body
        self.Response = requests.post(self.url, json=body, headers=self.headers)
        self.build_response()

    def patch(self, body=None):
        self.body = body
        self.Response = requests.patch(self.url, json=body, headers=self.headers)
        self.build_response()
