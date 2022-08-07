import requests, json

f = open("bitaps_addr.json")
data = json.load(f)

print(len(data["data"]["list"]))
