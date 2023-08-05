import http.client
import json

from payout.create_payout_account import CreatePayoutAccount
from payout.update_payout_account import UpdatePayoutAccount
from payout.find_payout_account import FindPayoutAccount
from payout.add_payout_token import AddPayoutToken
from payout.add_payout_rate import AddPayoutRate
from payout.start_payouts import StartPayouts
from payout.stop_payouts import StopPayouts


class Payout:
    def __init__(self, app, key) -> None:
        self.app = app
        self.key = key
        # Get app endpoints
        conn = http.client.HTTPSConnection("reddash.azurewebsites.net")
        route = "/app/endpoints/" + self.app
        headers = {"Accept": "application/json"}
        conn.request("POST", route, "", headers)
        response = json.loads(conn.getresponse().read().decode())
        # Parse and set dataEndpoints
        if "dataEndpoints" in response:
            self.dataEndpoints = response["dataEndpoints"]
        else:
            self.dataEndpoints = "ERROR Unable to get dataEndpoints from server"
        # Parse and set redpayEndpoints
        if "redpayEndpoints" in response:
            self.redpayEndpoints = response["redpayEndpoints"]
        else:
            self.redpayEndpoints = "ERROR Unable to get redpayEndpoints from server"

    def CreatePayoutAccount(self, request):
        request["app"] = self.app
        create_payout_account = CreatePayoutAccount(
            self.app, self.key, self.dataEndpoints)
        return create_payout_account.Process(request)

    def UpdatePayoutAccount(self, request):
        request["app"] = self.app
        update_payout_account = UpdatePayoutAccount(
            self.app, self.key, self.dataEndpoints)
        return update_payout_account.Process(request)

    def FindPayoutAccount(self, request):
        request["app"] = self.app
        find_payout_account = FindPayoutAccount(
            self.app, self.key, self.dataEndpoints)
        return find_payout_account.Process(request)

    def AddPayoutRate(self, request):
        request["app"] = self.app
        request["account"] = request["id"]
        add_payout_rate = AddPayoutRate(
            self.app, self.key, self.dataEndpoints)
        return add_payout_rate.Process(request)

    def AddPayoutToken(self, request):
        request["app"] = self.app
        request["account"] = request["id"]
        add_payout_token = AddPayoutToken(
            self.app, self.key, self.dataEndpoints)
        return add_payout_token.Process(request)

    def StartPayouts(self, request):
        request["app"] = self.app
        request["account"] = request["id"]
        start_payouts = StartPayouts(
            self.app, self.key, self.dataEndpoints)
        return start_payouts.Process(request)

    def StopPayouts(self, request):
        request["app"] = self.app
        request["account"] = request["id"]
        stop_payouts = StopPayouts(
            self.app, self.key, self.dataEndpoints)
        return stop_payouts.Process(request)
