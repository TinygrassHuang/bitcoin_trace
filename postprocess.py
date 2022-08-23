import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class Postprocessor:
    data: pd.DataFrame = None
    num_addr: int = None
    mode_label: str = None
    most_amount_label: str = None
    label_amount = {}
    address: str = None
    depth: int = None
    min: float = None

    def __init__(self, addr: str, depth: int, min: float):
        self.address = addr
        self.depth = depth
        self.min = min
        self.data = pd.read_csv(f"result/{addr}_{depth}_{min}.csv")
        self.num_addr = len(self.data["source_address"])
        self.mode_label = self.data["label"].value_counts().idxmax()

        label_amount = self.data.groupby(["label"]).sum()["amount"]
        self.most_amount_label = str(label_amount.idxmax())

        labels = ['exchanges', 'pool', 'services_others', 'gambling', 'darknet']
        for i in labels:
            if i in label_amount:
                self.label_amount[i] = label_amount[i]
            else:
                self.label_amount[i] = 0

    def print_data(self):
        print(self.data)
        print("-------------------------------------")

    def print_data_info(self):
        print("Number of addresses:", self.num_addr)
        print("Label with most amount:", self.most_amount_label)
        print("Most frequent label (mode):", self.mode_label)
        print("Amount list:")
        for key, value in self.label_amount.items():
            print(f"    {key}: {value:.8f} btc")

    def plot(self, save=False):
        colours = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        key = list(self.label_amount.keys())
        value = list(self.label_amount.values())
        fraction = [i / sum(value) for i in value]

        none_0_index = [i for i in range(len(value)) if value[i] != 0]
        print([value[i] for i in none_0_index])

        fig, ax = plt.subplots()
        ax.pie([fraction[i] for i in none_0_index],
               labels=[key[i] for i in none_0_index],
               autopct='%1.1f%%',
               textprops={"fontsize": 12},
               startangle=90,
               wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
               colors=[colours[i] for i in none_0_index])

        ax.axis("equal")
        plt.suptitle(f"Estimated Source of Bitcoin", fontsize=15)
        plt.title(self.address, fontsize=10)
        plt.legend(bbox_to_anchor=(1, 0), loc="lower right",
                   bbox_transform=plt.gcf().transFigure)
        plt.show()

        if save:
            fig.savefig(f"result/{self.address}_{self.depth}_{self.min}.jpg")


if __name__ == "__main__":
    address = "bc1qmxjefnuy06v345v6vhwpwt05dztztmx4g3y7wp"
    trace_depth = 5
    pp = Postprocessor(address, trace_depth,100 * 100000000 * 0.00000001)
    pp.print_data()
    pp.print_data_info()
    pp.plot(save=True)
