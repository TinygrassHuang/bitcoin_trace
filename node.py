from transactions import Transaction


class TransactionNode:
    tx_id: str = None
    amount: float = None
    source = []
    source_amount = []
    depth: int = None
    trans: Transaction = None

    def __init__(self, tx_id: str, amount: float, depth: int, max_depth: int):
        print(f"Create node: {tx_id}")
        print(f"depth: {depth}")
        self.tx_id = tx_id
        self.amount = amount
        self.trans = Transaction(self.tx_id)
        self.depth = depth
        if self.depth < max_depth:
            self.__grow_backward_tree(max_depth)

    def __grow_backward_tree(self, max_depth):
        for i in self.trans.input:
            prev_txid = i[2]
            prev_amount = self.amount * float(i[1]) / self.trans.total_input
            self.source_amount.append(prev_amount)
            t = TransactionNode(prev_txid, prev_amount, self.depth + 1, max_depth)
            self.source.append(t)

    def transverse(self, depth: int, percentage: float, max_depth: int):
        if depth == max_depth:
            return [row[0] for row in self.trans.output]  # all the addresses at the end
            # source and percentage list


if __name__ == "__main__":
    txid = "e2bfab9261020fc7e2f0742c010c05590fab4510fc041fc111146d17bc2c5c23"
    BTC = 47.78333906
    source = TransactionNode(txid,BTC,0,5)
