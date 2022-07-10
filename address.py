from math import ceil

import requests
import time
from bs4 import BeautifulSoup

request_interval = 3


def make_request_and_sleep(url) -> str:
    html = requests.get(url)

    if html.status_code == 200:
        html_text = html.text
        time.sleep(request_interval)
        return html_text
    else:
        print(html)
        raise requests.exceptions.HTTPError


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

    # def __scrap_transactions_with_count(self, count):
    #     # scrap number of transactions on first page
    #     if count > 100:
    #         print("Can only scrap 100 transactions")
    #         return
    #     if len(self.transactions) == 0:
    #         transactions = self.first_page.find_all('tr', {'class': ['sent', 'received']})
    #         i = 0
    #         for trans in transactions:
    #             self.__extract_transaction_info(trans)
    #             i += 1
    #             if i == count:
    #                 return

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
    bitcoin_address = "3LaNNTg87XjTtXAqs55WV5DyWASEZizCXZ"
    my_address = BitcoinAddress(bitcoin_address)
    my_address.print_all_transactions()
    print(my_address.total_trans)
    print(len(my_address.transactions))
    my_address.scrap_all_transactions()
    print(len(my_address.transactions))
