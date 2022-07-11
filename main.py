from bs4 import BeautifulSoup
import requests,time

# request interval: 1s(sometimes) 2s(okay)

# 3LaNNTg87XjTtXAqs55WV5DyWASEZizCXZ
# 1JdzjkxN9pAhmfRT6148UHsAPLM4QPYPqu
# 1Lm8VUCnqUFy6CcQyntcc3kd9o949UPR9f BlackBankMarket
bitcoin_address = "1JdzjkxN9pAhmfRT6148UHsAPLM4QPYPqu"
url = 'https://www.walletexplorer.com/address/' + bitcoin_address
html = requests.get(url)
print(html)
html_text = html.text
soup = BeautifulSoup(html_text, 'lxml')


wallet = soup.find('div', class_='walletnote').a.text
print(wallet)
wallet = wallet[1:-1]
print(wallet)

transactions = soup.find_all('tr', {'class': ['sent', 'received']})

for trans in transactions:
    date = trans.find('td', class_='date').text
    amount_diff = trans.find('td', class_='amount diff').text
    balance = trans.find('td', class_='amount').next_sibling.text
    txid = trans.find('td', class_='txid').text
    # print(date,amount_diff,balance,txid)

print(transactions[0].text)
print(len(transactions))
# date = transactions[0].find('td', class_='date').text
# amount_diff = transactions[0].find('td', class_='amount diff').text
# balance = transactions[0].find('td', class_='amount').next_sibling.text
# txid = transactions[0].find('td', class_='txid').text
# print(date,amount_diff,balance,txid)

txid = "6ec70ac1f3ad95047a47972997f93ad35a21d34700b0a7c481e5a5fac6c559fc"
tx_url = "https://www.walletexplorer.com/txid/" + txid
tx_html = requests.get(tx_url).text
tx_soup = BeautifulSoup(tx_html,"lxml")
table = tx_soup.find_all("table", class_="empty")
input_list = table[0]
output_list = table[1]

info = tx_soup.find("table", class_="info")
print(info("td")[2].text) # time
print(info("td")[3].text) # sender
print(info("td")[4].text) # fee

for member in output_list("tr"):
    info = member("td")
    addr = info[0].a.text
    wallet = info[1].text
    if wallet[0] == "[":
        wallet = wallet[1:-1]
    amount = info[2].text[:-3]
    if info[3].text == "unspent":
        flow = info[3].text
    else:
        flow = info[3].a["href"][6:]
    print(addr)
    print(wallet)
    print(amount)
    print(flow)

for member in input_list("tr"):
    info = member("td")
    addr = info[0].a.text
    amount = info[1].text[:-3]
    flow = info[2].a["href"][6:]
    print(addr)
    print(amount)
    print(flow)

abc = tx_soup.find("table", class_="tx").span.text
print(f"......{abc[1:-5]}......")

# print(output_list.find_all("tr")[0].text)
# print(output_list.find_all("td")[0])
# print(output_list.find_all("td")[1])
# print(output_list.find_all("td")[2])
# print(output_list.find_all("td")[3])
# i = 0
# bitcoin_address = "1JdzjkxN9pAhmfRT6148UHsAPLM4QPYPqu"
# url = 'https://www.walletexplorer.com/address/' + bitcoin_address
# start = time.time()
# while(i < 60):
#     html_text = requests.get(url)
#     print(html_text)
#     i += 1
#     print(i)
#     # time.sleep(1)
# end = time.time()
# print(end - start)
