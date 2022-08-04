from transactions import Transaction


class TransactionNode:
    tx_id: str = None
    amount: float = None
    min_amount: float = None
    source = None
    source_amount = None
    depth: int = None
    max_depth: int = None
    trans: Transaction = None
    final_src_addr_list = []
    final_src_amount_list = []
    leaf: bool = False

    def __init__(self, tx_id: str, amount: float, min_amount: float, max_depth: int, depth: int = 0):
        print(f"depth: {depth}")
        print(f"Create node: {tx_id}")
        print("amount:", amount)
        print("--------------------------")

        self.tx_id = tx_id
        self.amount = amount
        self.min_amount = min_amount
        self.trans = Transaction(self.tx_id)
        self.depth = depth
        self.max_depth = max_depth
        if self.depth == self.max_depth or self.leaf is True:
            self.leaf = True
            return
        self.__grow_tree()

    def __grow_tree(self):
        source = []
        source_amount = []
        for input in self.trans.input:
            prev_txid = input[2]
            prev_amount = self.amount * float(input[1]) / self.trans.total_input
            source_amount.append(prev_amount)
            if prev_amount > self.min_amount:
                self.leaf = False
                source.append(TransactionNode(prev_txid, prev_amount, self.min_amount, max_depth=self.max_depth,
                                              depth=self.depth + 1))
            else:
                self.leaf = True
        self.source = source
        self.source_amount = source_amount

    def get_source(self):
        # transverse the tree and reach the leaf node, return input list and respective amount
        self.__transverse_get_source()
        address_map = self.__prettify()

        self.final_src_addr_list = [addr for addr in address_map.keys()]
        self.final_src_amount_list = [amount for amount in address_map.values()]

        return self.final_src_addr_list, self.final_src_amount_list

    def __prettify(self):
        # eliminate duplication in addresses and round value to 8 decimal places (1 satoshi)
        address_map = {}
        for i in range(len(self.final_src_addr_list)):
            key = self.final_src_addr_list[i]
            value = round(self.final_src_amount_list[i], 8)
            if value == 0:
                continue
            if key in address_map:
                address_map[key] = address_map[key] + value
            else:
                address_map[key] = value
        return address_map

    def __transverse_get_source(self):
        # if self.source is None:
        if self.leaf is True:
            addr_list = [input[0] for input in self.trans.input]
            amount_list = [float(input[1]) for input in self.trans.input]
            amount_list = [value * self.amount / self.trans.total_input for value in amount_list]
            return addr_list, amount_list

        final_src_addr_list = []
        final_src_amount_list = []
        for i in self.source:
            [sub_addr_list, sub_amount_list] = i.__transverse_get_source()
            final_src_addr_list = final_src_addr_list + sub_addr_list
            final_src_amount_list = final_src_amount_list + sub_amount_list
        self.final_src_addr_list = final_src_addr_list
        self.final_src_amount_list = final_src_amount_list
        return self.final_src_addr_list, self.final_src_amount_list


if __name__ == "__main__":
    # e159bd642ce8e7319d37f6b32456a59db02d7209871ae0baf2ee9bdf0283b67d
    # e2bfab9261020fc7e2f0742c010c05590fab4510fc041fc111146d17bc2c5c23
    # 3870a9c90877dd5655861d52fe57effabb29ca490a15d3c510c79140f5052bb0
    txid = "3870a9c90877dd5655861d52fe57effabb29ca490a15d3c510c79140f5052bb0"
    BTC = 0.00001
    min_amount = 0.00000001
    source = TransactionNode(txid, BTC, min_amount, max_depth=5)
    [addr_list, amount_list] = source.get_source()
    print("final addr", addr_list)
    print("final amount", amount_list)
    print(sum(amount_list))
