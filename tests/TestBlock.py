import unittest

from src.Block import calculate_new_block_bits


class TestBlock(unittest.TestCase):
    def test_target_to_bits(self):
        str_blocks = [
            # Old
            "000000203471101bbda3fe307664b3283a9ef0e97d9a38a7eacd8800000000000000000010c8aba8479bbaa5e0848152fd3c2289ca50e1c3e58c9a4faaafbdf5803c5448ddb845597e8b0118e43a81d3",
            # New
            "02000020f1472d9db4b563c35f97c428ac903f23b7fc055d1cfc26000000000000000000b3f449fcbe1bc4cfbcb8283a0d2c037f961a3fdf2b8bedc144973735eea707e1264258597e8b0118e5f00474"
        ]

        bits = calculate_new_block_bits(str_blocks[1], str_blocks[0])
        self.assertEqual("80df6217", bits)


if __name__ == '__main__':
    unittest.main()
