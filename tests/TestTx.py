import unittest
from io import BytesIO
from src.tx.Tx import Tx


class TestTxParsing(unittest.TestCase):
    # TODO Correct Test
    def test_parsing(self):
        tx_hex = "010000000456919960ac691763688d3d3bcea9ad6ecaf875df5339e148a1fc61c6ed7a069e0100" \
                 "00006a47304402204585bcdef85e6b1c6af5c2669d4830ff86e42dd205c0e089bc2a821657e951" \
                 "c002201024a10366077f87d6bce1f7100ad8cfa8a064b39d4e8fe4ea13a7b71aa8180f012102f0" \
                 "da57e85eec2934a82a585ea337ce2f4998b50ae699dd79f5880e253dafafb7feffffffeb8f51f4" \
                 "038dc17e6313cf831d4f02281c2a468bde0fafd37f1bf882729e7fd3000000006a473044022078" \
                 "99531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc26125022008b422690b84" \
                 "61cb52c3cc30330b23d574351872b7c361e9aae3649071c1a7160121035d5c93d9ac96881f19ba" \
                 "1f686f15f009ded7c62efe85a872e6a19b43c15a2937feffffff567bf40595119d1bb8a3037c35" \
                 "6efd56170b64cbcc160fb028fa10704b45d775000000006a47304402204c7c7818424c7f7911da" \
                 "6cddc59655a70af1cb5eaf17c69dadbfc74ffa0b662f02207599e08bc8023693ad4e9527dc42c3" \
                 "4210f7a7d1d1ddfc8492b654a11e7620a0012102158b46fbdff65d0172b7989aec8850aa0dae49" \
                 "abfb84c81ae6e5b251a58ace5cfeffffffd63a5e6c16e620f86f375925b21cabaf736c779f88fd" \
                 "04dcad51d26690f7f345010000006a47304402200633ea0d3314bea0d95b3cd8dadb2ef79ea833" \
                 "1ffe1e61f762c0f6daea0fabde022029f23b3e9c30f080446150b23852028751635dcee2be669c" \
                 "2a1686a4b5edf304012103ffd6f4a67e94aba353a00882e563ff2722eb4cff0ad6006e86ee20df" \
                 "e7520d55feffffff0251430f00000000001976a914ab0c0b2e98b1ab6dbf67d4750b0a56244948" \
                 "a87988ac005a6202000000001976a9143c82d7df364eb6c75be8c80df2b3eda8db57397088ac46" \
                 "430600"

        # Convert hex to bytes and parse the transaction
        tx_bytes = BytesIO(bytes.fromhex(tx_hex))
        tx = Tx.parse(tx_bytes)

        # Extract required fields
        script_sig_2nd_input = tx.tx_ins[1].script_sig  # Second input
        script_pubkey_1st_output = tx.tx_outs[0].script_pubkey  # First output
        amount_2nd_output = tx.tx_outs[1].amount  # Second output amount

        # Expected values (from manual parsing or a blockchain explorer)
        expected_script_sig_2nd_input = (
            "47304402207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc26125"
            "022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae3649071c1a71601"
            "21035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872e6a19b43c15a2937"
        )
        expected_script_pubkey_1st_output = "76a914ab0c0b2e98b1ab6dbf67d4750b0a56244948a87988ac"
        expected_amount_2nd_output = 381010  # 0x5A6202 in little-endian

        # Assert the extracted values
        self.assertEqual(script_sig_2nd_input.serialize().hex(), expected_script_sig_2nd_input)
        self.assertEqual(script_pubkey_1st_output.serialize().hex(), expected_script_pubkey_1st_output)
        self.assertEqual(amount_2nd_output, expected_amount_2nd_output)


if __name__ == '__main__':
    unittest.main()
