import json
import textwrap
import time

from util import make_request_and_sleep


class Transaction:
    txid: str = None
    url: str = None
    fee: float = None
    total_input: float = None
    input = None
    output = None
    is_coinbase = False

    def __init__(self, txid: str):
        self.txid = txid
        self.url = "https://www.walletexplorer.com/api/1/tx?txid=" + txid + "&caller=bitcoinTracerImperial"
        try:
            html = make_request_and_sleep(self.url)
        except:
            print("too fast, sleeping")
            time.sleep(10)
            html = make_request_and_sleep(self.url)
        info = json.loads(html)

        temp_input = []
        for member in info["in"]:
            addr = member["address"]
            amount = member["amount"]
            prev_tx = member["next_tx"]
            temp_input.append([addr, amount, prev_tx])

        temp_output = []
        for member in info["out"]:
            addr = member["address"]
            wallet = member["wallet_id"]
            amount = member["amount"]
            try:
                next_tx = member["next_tx"]
            except:
                next_tx = "unspent"
            temp_output.append([addr, wallet, amount, next_tx])

        self.input = temp_input
        self.output = temp_output
        self.total_input = sum([i[1] for i in self.input])
        if info['is_coinbase'] is True:
            self.is_coinbase = True
            self.input = "coinbase"
        else:
            self.fee = self.total_input - sum([i[2] for i in self.output])

    def __str__(self):
        return textwrap.dedent(f'''\
        txid: {self.txid}
        fee: {self.fee}
        input: {self.input}
        output: {self.output}
        ''')


if __name__ == "__main__":
    # 42945b585c662735e919fbae67b5c13eb6c08ccc1296796a43e464dbb8c193ce
    # 6ec70ac1f3ad95047a47972997f93ad35a21d34700b0a7c481e5a5fac6c559fc
    # 3870a9c90877dd5655861d52fe57effabb29ca490a15d3c510c79140f5052bb0
    # ff8e606d2ead80bc522e2fccad0ea11c8b0e85898d3702946dc39fac3279f0e4 coinbase transaction
    trans = Transaction("ff8e606d2ead80bc522e2fccad0ea11c8b0e85898d3702946dc39fac3279f0e4")
    print(trans)
    print([row[0] for row in trans.output])
    print("total input:",trans.total_input)
    print(len(trans.input))
    print(len(trans.output))
    # new_trans = Transaction("3870a9c90877dd5655861d52fe57effabb29ca490a15d3c510c79140f5052bb0")
    # print(trans.input)
    # print(new_trans.input)
