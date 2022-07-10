import requests, json

# try to query transaction data using JSON

"""
Blockchain.com data API

Single Block
https://blockchain.info/rawblock/$block_hash

Single Transaction
https://blockchain.info/rawtx/$tx_hash

Chart Data
https://blockchain.info/charts/$chart-type?format=json

Block Height
https://blockchain.info/block-height/$block_height?format=json

Single Address
https://blockchain.info/rawaddr/$bitcoin_address

Multi Address
https://blockchain.info/multiaddr?active=$address|$address

Unspent Outputs
https://blockchain.info/unspent?active=$address

Balance
https://blockchain.info/balance?active=$address

Latest Block
https://blockchain.info/latestblock

Blocks
Blocks for one day: https://blockchain.info/blocks/$time_in_milliseconds?format=json
Blocks for specific pool: https://blockchain.info/blocks/$pool_name?format=json

"""

# wrong_address = "3LaNNTg87XjTtXAqs55WV5DyWASEZizCXA"
# address = "3LaNNTg87XjTtXAqs55WV5DyWASEZizCXZ"
# # address = "1Lm8VUCnqUFy6CcQyntcc3kd9o949UPR9f"
#
# url = "https://blockchain.info/rawaddr/"
# html_text = requests.get(url + address).text
# data = json.loads(html_text)
# print(len(data['txs']))
# print(type(data['txs']))
# print(data['n_unredeemed'])
#
# for tx in data['txs']:
#     for o in tx['out']:
#         if o['addr'] == address and o['spent'] is False:
#             print(o['addr'])
#             print(tx['hash'])

unspent_data = requests.get("https://blockchain.info/unspent?active=1Lm8VUCnqUFy6CcQyntcc3kd9o949UPR9f").text
unspent_data = json.loads(unspent_data)
print(json.dumps(unspent_data,indent=2))

for tx in unspent_data['unspent_outputs']:
    tx_id = tx["tx_hash_big_endian"]
    print(tx_id)

wrong_response = requests.get("https://www.blockchain.com/btc/address/1Lm8VUCnqUFy6CcQyntcc3kd9o949UPR9D")
print(f"Should be wrong: {wrong_response}")

url = "https://blockchain.info/q/addressbalance/1Lm8VUCnqUFy6CcQyntcc3kd9o949UPR9f?confirmations=6"
balance = requests.get(url).text
print(balance)
