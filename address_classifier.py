import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from util import compute_5_feature, make_request_and_sleep
import keras.models, joblib,json,requests,time
import numpy as np


class AddressClassifier:
    label_encoder = None
    standard_scaler = None
    model = None

    def __init__(self):
        self.label_encoder = joblib.load("LabelEncoder.pkl")
        self.standard_scaler = joblib.load("StandardScaler.pkl")
        self.model = keras.models.load_model("bitcoin_address_classifier.h5")

    def classify(self, addr):
        feature = self.get_bitcoin_address_feature(addr)
        time.sleep(10)
        feature = self.standard_scaler.transform(feature.reshape(1, -1))
        prediction = np.argmax(self.model.predict(feature, verbose=0), axis=1)
        return self.label_encoder.inverse_transform(prediction)[0]

    # run with 10s interval
    def get_bitcoin_address_feature(self,addr: str):
        url = "https://blockchain.info/rawaddr/" + addr
        html = requests.get(url)
        text = html.text
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

        return np.array([n_transactions] + [block_height_max_min] + fee + [
            max(fee_ls) - min(fee_ls)] + size + weight + vin_sz + vout_sz + inputs + outputs)


if __name__ == "__main__":
    addr = "1136GYGTdySKCocdjqZphXiW4zoskXHqML"
    my_classifier = AddressClassifier()
    feature = my_classifier.get_bitcoin_address_feature(addr)
    print(feature)
    print(my_classifier.classify(addr))
