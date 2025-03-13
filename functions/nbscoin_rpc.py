import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

NBSCOIN_RPC_USER = os.getenv("NBSCOIN_RPC_USE")
NBSCOIN_RPC_PASSWORD = os.getenv("NBSCOIN_RPC_PASSWORD")
NBSCOIN_RPC_HOST = os.getenv("NBSCOIN_RPC_HOST")
NBSCOIN_RPC_PORT = os.getenv("NBSCOIN_RPC_PORT")

class NBScoinRPC:
    def __init__(self):
        self.url = f"http://{NBSCOIN_RPC_USER}:{NBSCOIN_RPC_PASSWORD}@{NBSCOIN_RPC_HOST}:{NBSCOIN_RPC_PORT}"
        print(self.url)
        self.headers = {'content-type': 'application/json'}

    def call(self, method, params=None):
        payload = {
            "method": method,
            "params": params or [],
            "jsonrpc": "2.0",
            "id": 1,
        }
        response = requests.post(self.url, data=json.dumps(payload), headers=self.headers).json()
        return response.get('result')

    def get_balance(self, account=None):
        return self.call('getbalance', [account] if account else [])

    def get_new_address(self):
        return self.call('getnewaddress')

    def send_to_address(self, address, amount):
        return self.call('sendtoaddress', [address, amount])

    def list_transactions(self, account="*", count=10):
        return self.call('listtransactions', [account, count])

    def get_transaction(self, txid):
        return self.call('gettransaction', [txid])


