import json
import time

import requests
from my_token import bitcoinAbuseToken


class ReportSearcher:
    abuse_types = {}
    result = {}

    def __init__(self):
        type_url = "https://www.bitcoinabuse.com/api/abuse-types"
        data = json.loads(requests.get(type_url).text)
        for i in data:
            id = i['id']
            label = i['label']
            self.abuse_types[id] = label

    def check_bitcoin_abuse(self, addr_list: list[str]):
        for addr in addr_list:
            url = f"https://www.bitcoinabuse.com/api/reports/check?address={addr}&api_token={bitcoinAbuseToken}"
            text = requests.get(url).text
            data = json.loads(text)
            count = data['count']
            if count > 0:
                self.result[addr] = count
            time.sleep(2)
        print("----------------------------")
        print(f"Total {len(addr_list)} address(es) received to search on BitcoinAbuse.com.")
        if self.result:
            print(f"Total {sum(self.result.values())} report(s) found in {len(self.result)} address(es)")
            print("Address -- report count:")
            for key, value in self.result.items():
                print(f"{key} -- {value}")
        else:
            print("No reports found")


if __name__ == "__main__":
    # bc1qmxjefnuy06v345v6vhwpwt05dztztmx4g3y7wp  6 reports on BitcoinAbuse
    address_list = ["bc1qe46q4eumhc8tj0vf9czu56sp9yas4635k4z4rr",
                    #"bc1qmxjefnuy06v345v6vhwpwt05dztztmx4g3y7wp",
                    #"1ArJTD4iR3SCwjuyiP3H6pbwvPBHduX6WB"
                    ]
    sr = ReportSearcher()
    sr.check_bitcoin_abuse(address_list)

