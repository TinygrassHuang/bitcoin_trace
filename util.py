import json

import keras.models, joblib
import numpy as np
from math import ceil

import requests
import time
from bs4 import BeautifulSoup

request_interval = 0.5


def make_request_and_sleep(url) -> str:
    time.sleep(request_interval)
    html = requests.get(url)

    if html.status_code == 200:
        html_text = html.text
        return html_text
    else:
        print(html)
        raise requests.exceptions.HTTPError


# run 10 seconds a time
def get_bitcoin_address_feature(addr: str):
    url = "https://blockchain.info/rawaddr/" + addr
    text = make_request_and_sleep(url)
    data = json.loads(text)

    n_transactions = data["n_tx"]
    tx_ls = data["txs"]

    block_height_ls = []
    fee_ls = []
    size_ls = []
    weight_ls = []
    vin_sz_ls = []
    vout_sz_ls = []
    input_ls = []
    output_ls = []

    for tx in tx_ls:
        block_height = tx["block_height"]
        block_height_ls.append(block_height)
        fee = tx["fee"]
        fee_ls.append(fee)
        size = tx["size"]
        size_ls.append(size)
        weight = tx["weight"]
        weight_ls.append(weight)
        vin_sz = tx["vin_sz"]
        vin_sz_ls.append(vin_sz)
        vout_sz = tx["vout_sz"]
        vout_sz_ls.append(vout_sz)

        input_amount = 0
        for i in tx["inputs"]:
            input_amount += i["prev_out"]["value"]
        input_ls.append(input_amount)

        output_amount = 0
        for o in tx["out"]:
            output_amount += o["value"]
        output_ls.append(output_amount)

    block_height_max_min = max(block_height_ls) - min(block_height_ls)
    fee = compute_5_feature(fee_ls)
    size = compute_5_feature(size_ls)
    weight = compute_5_feature(weight_ls)
    vin_sz = compute_5_feature(vin_sz_ls)
    vout_sz = compute_5_feature(vout_sz_ls)
    inputs = compute_5_feature(input_ls)
    outputs = compute_5_feature(output_ls)

    return [n_transactions] + [block_height_max_min] + fee + [
        max(fee_ls) - min(fee_ls)] + size + weight + vin_sz + vout_sz + inputs + outputs


# ['coinjoin-like' 'exchange' 'gambling' 'miner' 'mining_pool' 'services']
def classify(addr: str):
    label_encoder = joblib.load("LabelEncoder.pkl")
    standard_scaler = joblib.load("StandardScaler.pkl")
    model = keras.models.load_model("bitcoin_address_classifier.h5")
    feature = get_bitcoin_address_feature(addr)
    feature = standard_scaler.transform(feature)
    prediction = np.argmax(model.predict(feature), axis=1)
    return label_encoder.inverse_transform([prediction])[0]


def compute_5_feature(feature_ls):
    ls = [np.mean(feature_ls),
          np.median(feature_ls),
          np.std(feature_ls),
          min(feature_ls),
          max(feature_ls)]
    ls = [round(i, 4) for i in ls]
    return ls


class BitcoinAddress:
    address = None
    wallet = None
    url = None
    first_page = None
    total_trans = None
    transactions = []  # transaction history of an address, not the same as class Transaction

    def __init__(self, address: str):
        self.address = address
        self.url = 'https://www.walletexplorer.com/address/' + address
        html_text = make_request_and_sleep(self.url)
        self.first_page = BeautifulSoup(html_text, 'lxml')
        self.wallet = self.first_page.find('div', class_='walletnote').a.text
        self.total_trans = int(self.first_page.find('div', class_='paging').small.text[21:-1].replace(',', ''))

    def scrap_all_transactions(self):
        if len(self.transactions) != 0:
            print("Transactions already scraped")
            return
        # scrape all transaction history
        No_of_pages = ceil(self.total_trans / 100)
        if No_of_pages > 1:
            for i in range(1, No_of_pages):
                url = self.url + '?page=' + str(i + 1)
                print(f"Request page: {i + 1}")
                html = make_request_and_sleep(url)
                soup = BeautifulSoup(html, 'lxml')
                self.__scrap_transactions_on_page(soup)
        else:
            self.__scrap_transactions_on_page(self.first_page)

    def __scrap_transactions_on_page(self, soup: BeautifulSoup):
        # scrap all transactions in one page
        transactions = soup.find_all('tr', {'class': ['sent', 'received']})
        for trans in transactions:
            self.__extract_transaction_info(trans)

    def __extract_transaction_info(self, trans):
        date = trans.find('td', class_='date').text
        amount_diff = trans.find('td', class_='amount diff').text.strip()
        balance = trans.find('td', class_='amount').next_sibling.text.strip()
        txid = trans.find('td', class_='txid').text
        transaction = [date, amount_diff, balance, txid]
        self.transactions.append(transaction)

    def print_all_transactions(self):
        print(f"Total number of transactions made: {self.total_trans}")
        if len(self.transactions) == 0:
            print("No transaction stored")
        else:
            for trans in self.transactions:
                print(trans)


if __name__ == "__main__":
    # bitcoin_address = "3LaNNTg87XjTtXAqs55WV5DyWASEZizCXZ"
    # my_address = BitcoinAddress(bitcoin_address)
    # my_address.print_all_transactions()
    # print(my_address.total_trans)
    # print(len(my_address.transactions))
    # my_address.scrap_all_transactions()
    # print(len(my_address.transactions))
    addr = "114ADriuRWjkdmADR1wfL4KDqttNxGjp3D"
    # feature = get_bitcoin_address_feature(addr)
    # print(feature)
    # print(len(feature))
    print(classify(addr))
