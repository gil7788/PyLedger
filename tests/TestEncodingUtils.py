import unittest

from src.utils.encoding_utils import *


class TestEncodingUtils(unittest.TestCase):
    def test_base58(self):
        value = "f3k5U8nZr9H0w2xQlD7Vj4TzX6sGp1yYCmEoLFbWSaIqRAeJgtBihPvMcONK"
        # Convert string to bytes
        value_bytes = value.encode('utf-8')
        # Encode the bytes using base58
        value_encoded = encode_base58(value_bytes)
        # Decode the base58 encoded string
        value_decoded_bytes = decode_base58(value_encoded)
        # Convert bytes back to string
        value_decoded = value_decoded_bytes.decode('utf-8')
        self.assertEqual(value, value_decoded)
