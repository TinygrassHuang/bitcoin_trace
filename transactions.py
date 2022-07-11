import requests
import textwrap
from bs4 import BeautifulSoup
from address import make_request_and_sleep


class Transaction:
    txid = None
    url = None
    time = None
    sender = None
    fee = None
    total_input: float = None
    soup = None
    input = None
    output = None

    def __init__(self, txid: str):
        self.txid = txid
        self.url = "https://www.walletexplorer.com/txid/" + txid
        html = make_request_and_sleep(self.url)
        self.soup = BeautifulSoup(html, "lxml")
        info = self.soup.find("table", class_="info")
        self.time = info("td")[2].text
        self.sender = info("td")[3].text
        self.fee = info("td")[4].text
        self.total_input = float(self.soup.find("table", class_="tx").span.text[1:-5])

        table = self.soup.find_all("table", class_="empty")
        input_list = table[0]
        output_list = table[1]

        temp_input = []
        temp_output = []
        for member in input_list("tr"):
            info = member("td")
            addr = info[0].a.text
            amount = info[1].text[:-3].strip()
            flow = info[2].a["href"][6:]
            temp_input.append([addr, amount, flow])

        for member in output_list("tr"):
            info = member("td")
            try:
                addr = info[0].a.text
            except:
                continue
            wallet = info[1].text
            if wallet[0] == "[":
                wallet = wallet[1:-1]
            amount = info[2].text[:-3].strip()
            if info[3].text == "unspent":
                flow = info[3].text
            else:
                flow = info[3].a["href"][6:]
            temp_output.append([addr, wallet, amount, flow])

        self.input = temp_input
        self.output = temp_output

    def __str__(self):
        return textwrap.dedent(f'''\
        txid: {self.txid}
        time: {self.time}
        sender: {self.sender}
        fee: {self.fee}
        input: {self.input}
        output: {self.output}
        ''')


if __name__ == "__main__":
    # 42945b585c662735e919fbae67b5c13eb6c08ccc1296796a43e464dbb8c193ce
    # 6ec70ac1f3ad95047a47972997f93ad35a21d34700b0a7c481e5a5fac6c559fc
    trans = Transaction("42945b585c662735e919fbae67b5c13eb6c08ccc1296796a43e464dbb8c193ce")
    # print(trans)
    # print([row[0] for row in trans.output])
    # print(trans.total_input)
    # print("old",len(trans.input))
    new_trans = Transaction("6ec70ac1f3ad95047a47972997f93ad35a21d34700b0a7c481e5a5fac6c559fc")
    print(len(trans.input))
    print(len(new_trans.input))
