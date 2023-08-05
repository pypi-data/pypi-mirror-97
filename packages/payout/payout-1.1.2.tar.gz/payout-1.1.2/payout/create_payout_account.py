import http.client
import urllib.parse as urlparse
import json


class CreatePayoutAccount:
    def __init__(self, app, key, endpoint) -> None:
        self.app = app
        self.key = key
        self.endpoint = endpoint
        self.route = "/payoutaccount/create"

    def Process(self, request):
        json_data = json.dumps(request)
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
            conn.request('POST', self.route, json_data, headers)
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
