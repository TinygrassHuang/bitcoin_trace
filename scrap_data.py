import json
import time
import requests
from address_classifier import AddressClassifier
import pandas as pd
from os.path import exists

# total 10000 addresses:
# 5 classes, 2000 addr per class, 10 entities per class
# 200 addr per entity


# Exchanges:
"""
Huobi.com", "Huobi.com-2", "Bittrex.com", "Luno.com", "Poloniex.com",
"Kraken.com", "Binance.com", "MercadoBitcoin.com.br",
"Bitstamp.net", "Cex.io
"""

# Pools:
"""
BTCCPool", "SlushPool.com", "SlushPool.com-old", "SlushPool.com-old2",
"AntPool.com", "KnCMiner.com", "AntPool.com-old2", "BitMinter.com",
"GHash.io", "BW.com
"""

# Services/others:
"""
"CoinPayments.net", "Xapo.com", "Cryptonator.com", "Cubits.com", "HaoBTC.com",
"HelixMixer", "BTCJam.com", "GreenRoadMarket", "NucleusMarket",
"HelixMixer-old"
"""

# Gambling:
"""
"SatoshiDice.com", "SatoshiDice.com-original", "BitcoinVideoCasino.com",
"NitrogenSports.eu", "CoinGaming.io", "SatoshiMines.com",
"PrimeDice.com", "Betcoin.ag", "CoinRoyale.com", "SwCPoker.eu"
"""

# Darknet Market:
"""
"AgoraMarket", "SilkRoadMarketplace", "SilkRoad2Market", "SheepMarketplace",
"MiddleEarthMarketplace", "CannabisRoadMarket", "PandoraOpenMarket",
"AbraxasMarket", "BlueSkyMarketplace"
"""


def get_label_addresses(save=False):
    candidate = ["Huobi.com", "Huobi.com-2", "Bittrex.com", "Luno.com", "Poloniex.com",
                 "Kraken.com", "Binance.com", "MercadoBitcoin.com.br",
                 "Bitstamp.net", "Cex.io"]
    assert len(candidate) == 10  # 9 for darknet, 10 for others
    saveDF = pd.DataFrame(columns=["entity", "address"])
    for id in candidate:
        if id == "SheepMarketplace":
            page_count = [0, 100, 200, 300]
        else:
            page_count = [0, 100]
        for c in page_count:
            url = "https://www.walletexplorer.com/api/1/wallet-addresses?wallet=" + id + "&from=" + str(
                c) + "&count=100&caller=ImperialBitcoinTracer"
            text = requests.get(url).text
            data = json.loads(text)
            addr_ls = []
            for i in data["addresses"]:
                addr = i["address"]
                addr_ls.append(addr)

            print(id, len(addr_ls))
            if id != "AntPool.com-old2":  # this one only have 176
                assert len(addr_ls) == 100
            df = pd.DataFrame({"entity": [id] * len(addr_ls),
                               "address": addr_ls,
                               })
            saveDF = pd.concat([saveDF, df], ignore_index=True)
            time.sleep(0.5)

    print(saveDF)
    if save is True:
        saveDF.to_csv("data/exchanges.csv", index=False)


# 	n_transactions	block_height_max-min
# 	fee_mean	fee_median	fee_std	fee_min	fee_max	fee_max-min
# 	size_mean	size_median	size_std	size_min	size_max
# 	weight_mean	weight_median	weight_std	weight_min	weight_max
# 	vin_sz_mean	vin_sz_median	vin_sz_std	vin_sz_min	vin_sz_max
# 	vout_sz_mean	vout_sz_median	vout_sz_std	vout_sz_min	vout_sz_max
# 	inputsAmount_mean	inputsAmount_median	inputsAmount_std	inputsAmount_min	inputsAmount_max
# 	outputsAmount_mean	outputsAmount_median	outputsAmount_std	outputsAmount_min	outputsAmount_max
def compute_feature_sample(name: str):
    extra_header = ["n_transactions", "block_height_max-min",
                    "fee_mean", "fee_median", "fee_std", "fee_min", "fee_max", "fee_max-min",
                    "size_mean", "size_median", "size_std", "size_min", "size_max",
                    "weight_mean", "weight_median", "weight_std", "weight_min", "weight_max",
                    "vin_sz_mean", "vin_sz_median", "vin_sz_std", "vin_sz_min", "vin_sz_max",
                    "vout_sz_mean", "vout_sz_median", "vout_sz_std", "vout_sz_min", "vout_sz_max",
                    "inputsAmount_mean", "inputsAmount_median", "inputsAmount_std", "inputsAmount_min",
                    "inputsAmount_max",
                    "outputsAmount_mean", "outputsAmount_median", "outputsAmount_std", "outputsAmount_min",
                    "outputsAmount_max"]
    assert len(extra_header) == 38

    print(name)
    if exists("data/" + name + "_full.csv"):
        df = pd.read_csv("data/" + name + "_full.csv")
    else:
        df = pd.read_csv("data/" + name + ".csv")
        df["label"] = name
        df = df.reindex(df.columns.tolist() + extra_header, axis=1)

    while (df["n_transactions"].isna().any()):
        first_empty_index = df["n_transactions"].isna().argmax(axis=0)  # find where to start
        feature = AddressClassifier.get_bitcoin_address_feature(df.iloc[first_empty_index, 1])
        df.iloc[first_empty_index, 3:] = feature
        df.to_csv("data/" + name + "_full.csv", index=False)
        print(first_empty_index, "done")
        print(feature)
        print("------------------------------------")
        time.sleep(10)


def merge_all_data(save: bool):
    name = ['exchanges', 'pool', 'services_others', 'gambling', 'darknet']
    df = pd.concat([pd.read_csv("data/" + i + "_full.csv") for i in name], ignore_index=True)
    print(df.shape)
    if save:
        df.to_csv("data/new_full_data.csv")


if __name__ == "__main__":
    # check file name before saving
    # get_label_addresses(save=False)
    # name = ['exchanges', 'pool', 'services_others', 'gambling', 'darknet']
    # compute_feature_sample(name[2])
    merge_all_data(save=False)
