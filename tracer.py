import requests, json, time
from address import BitcoinAddress, make_request_and_sleep
from transactions import Transaction


# start tracing from addresses with little transactions
# para: -origin
# method: - trace source of money inside one address (trace back)
# - trace outflow of money from one address
# - label one address's entity by open source label (online source or social media),
# or do machine learning or DIY.
# - visualisation


def check_address(address: str) -> bool:
    url = "https://www.blockchain.com/btc/address/"
    html = requests.get(url + address)
    if html.status_code == 404:
        print(html)
        return False
    elif html.status_code == 200:
        return True
    print("Unexpected response:", html)
    return False


class BitcoinTracer:
    address: str = None
    unspent_transactions = []
    unspent_bitcoin = []
    depth: int = None

    def __init__(self, bitcoin_address: str, depth: int):
        if check_address(bitcoin_address) is False:
            raise ValueError("Illegal Bitcoin Address")
        self.address = bitcoin_address
        self.depth = depth
        if self.__check_zero_balance() is False:
            self.__request_unspent_transactions()
        else:
            print("0 balance, no need to check anything")

    def __check_zero_balance(self):
        url = "https://blockchain.info/q/addressbalance/" + self.address + "?confirmations=6"
        balance = requests.get(url).text
        if balance == "0":
            return True
        return False

    def __request_unspent_transactions(self):
        url = "https://blockchain.info/unspent?active="
        html_text = make_request_and_sleep(url + self.address)
        data = json.loads(html_text)
        for i in data['unspent_outputs']:
            tx_id = i["tx_hash_big_endian"]
            self.unspent_transactions.append(tx_id)
            self.unspent_bitcoin.append(float(i["value"]) / 100000000)

    def backward_trace(self, depth: int):
        for trans in self.unspent_transactions:
            self.transverse_tree(trans, depth)

    def transverse_tree(self, tx_id, depth):
        pass

    def forward_trace(self, depth: int):
        raise NotImplementedError


if __name__ == "__main__":
    # wrong_address = "3LaNNTg87XjTtXAqs55WV5DyWASEZizCXA"
    # address = "3LaNNTg87XjTtXAqs55WV5DyWASEZizCXZ"
    # print(f"Should return false: {check_address(wrong_address)}")
    # print(f"Should return true: {check_address(address)}")

    tracer = BitcoinTracer("1Lm8VUCnqUFy6CcQyntcc3kd9o949UPR9f", 2)
    for tx in tracer.unspent_transactions:
        print(tx)
    print(tracer.unspent_bitcoin)
