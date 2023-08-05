import http.client
import urllib.parse as urlparse
import json


class StartPayouts:
    def __init__(self, app, key, endpoint) -> None:
        self.app = app
        self.key = key
        self.endpoint = endpoint
        self.route = "/payoutstart/" + app + "/"

    def Process(self, request):
        account = ""
        if "account" in request:
            account = request["account"]
        else:
            return {
                "code": 400,
                "error": "account is required"
            }

        headers = {"Content-type": "application/json",
                   "Accept": "application/json"}

        url_info = urlparse.urlparse(self.endpoint)
        if url_info.scheme == "https":
            conn = http.client.HTTPSConnection(
                url_info.hostname, url_info.port or 443)
        else:
            conn = http.client.HTTPSConnection(
                url_info.hostname, url_info.port or 80)

        try:
            conn.request('POST', (self.route + account), "", headers)
            response = conn.getresponse()
            if response.status == 200:
                return json.loads(response.read().decode())
            else:
                return {
                    "code": response.status,
                    "error": response.reason
                }
        finally:
            conn.close()
