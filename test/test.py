import unittest
from address import BitcoinAddress

class MyTestCase(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, False)  # add assertion here

    bitcoin_address = "1JdzjkxN9pAhmfRT6148UHsAPLM4QPYPqu"

    def test_wallet_of_address(self):
        my_address = BitcoinAddress(self.bitcoin_address)
        self.assertEqual(my_address.wallet,"a89dd11a62")

    # test_illegal_address

    # test


if __name__ == '__main__':
    unittest.main()
