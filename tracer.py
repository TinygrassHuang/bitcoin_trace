import pandas as pd
import requests, json, time
from util import make_request_and_sleep, check_address
from node import TransactionNode
from address_classifier import AddressClassifier


class BitcoinTracer:
    address: str = None
    unspent_transactions = []
    unspent_bitcoin = []
    trace_depth: int = None
    addr_result = None
    btc_result = None
    min_amount: float = None  # smallest unit of btc during tracing
    classifier: AddressClassifier = None
    addr_label_result = None

    def __init__(self, bitcoin_address: str, trace_depth: int, min_amount: float = 0):
        if check_address(bitcoin_address) is False:
            raise ValueError("Illegal Bitcoin Address")
        self.address = bitcoin_address
        self.trace_depth = trace_depth
        if min_amount < 0.00000001:
            raise ValueError("Minimum amount cannot be smaller than 1 satoshi")
        else:
            self.min_amount = min_amount
        if self.__check_zero_balance() is False:
            self.__request_unspent_transactions()
        else:
            print("0 balance, no need to check anything")

        self.classifier = AddressClassifier()

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

    def trace(self):
        if self.addr_result is None:
            addr_result = []
            btc_result = []
            for i in range(len(self.unspent_transactions)):
                txid = self.unspent_transactions[i]
                btc = self.unspent_bitcoin[i]
                tree = TransactionNode(txid, btc, self.min_amount, self.trace_depth)
                [addr_list, amount_list] = tree.get_source()
                addr_result = addr_result + addr_list
                btc_result = btc_result + amount_list
            self.addr_result = addr_result
            self.btc_result = btc_result

        return self.addr_result, self.btc_result

    def classify_all_result_addr(self):
        if self.addr_result is None:
            print("You need to trace the money first!")
        else:
            print(f"Found {len(self.addr_result)} source address, might take around {len(self.addr_result)*10} seconds")
            address_label = []
            for i, addr in enumerate(self.addr_result):
                label = self.classifier.classify(addr)
                address_label.append(label)
                print(f"{i + 1} done")

            self.addr_label_result = address_label
            return self.addr_label_result

    def save_results(self):
        if self.addr_result is None or self.addr_label_result is None:
            print("You need to trace the money and classify results first")
        else:
            df = pd.DataFrame({"source_address": self.addr_result,
                               "amount": self.btc_result,
                               "label": self.addr_label_result,
                               })
            df.to_csv(f"result/{self.address}_{self.trace_depth}_{self.min_amount}.csv", index=False)
            print(f"Trace result saved to: result/{self.address}_{self.trace_depth}_{self.min_amount}.csv")


if __name__ == "__main__":
    # wrong_address = "3LaNNTg87XjTtXAqs55WV5DyWASEZizCXA"
    # address = "3LaNNTg87XjTtXAqs55WV5DyWASEZizCXZ"
    # print(f"Should return false: {check_address(wrong_address)}")
    # print(f"Should return true: {check_address(address)}")

    # 188VFs29DA34AVoPXsZWWacJ1aftxzL8Xm  0 balance
    # 1Lm8VUCnqUFy6CcQyntcc3kd9o949UPR9f
    # 1ArJTD4iR3SCwjuyiP3H6pbwvPBHduX6WB
    # 3LYJfcfHPXYJreMsASk2jkn69LWEYKzexb  a very rich address with 46 unspent txs
    # bc1qmxjefnuy06v345v6vhwpwt05dztztmx4g3y7wp another very rich address with 8 unspent
    tic = time.perf_counter()
    address = "bc1qmxjefnuy06v345v6vhwpwt05dztztmx4g3y7wp"
    trace_depth = 7
    min_amount = 100 * 100000000 * 0.00000001 # BTC
    tracer = BitcoinTracer(address, trace_depth, min_amount=min_amount)
    # for tx in tracer.unspent_transactions:
    #     print(tx)
    # print(tracer.unspent_bitcoin)
    print("number of unspent transactions", len(tracer.unspent_transactions))
    [source_addr, amount] = tracer.trace()
    for i in range(len(source_addr)):
        print(source_addr[i], amount[i])
    print("total number of source:", len(source_addr))
    toc = time.perf_counter()
    print(f"Time spent {toc - tic:0.4f} seconds")

    # label = tracer.classify_all_result_addr()
    # print(label)
    # tac = time.perf_counter()
    # print(f"Time spent {tac - toc:0.4f} seconds")

    # tracer.save_results()

