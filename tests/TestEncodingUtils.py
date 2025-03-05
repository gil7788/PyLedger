import unittest

from src.utils.encoding_utils import *


class TestEncodingUtils(unittest.TestCase):
    def test_base58_completeness(self):
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

    def test_encode58(self):
        testcases = (
            0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d.to_bytes(
                (0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d.bit_length() + 7) // 8, 'big'
            ),
            0xeff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c.to_bytes(
                (0xeff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c.bit_length() + 7) // 8, 'big'
            ),
            0xc7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6.to_bytes(
                (0xc7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6.bit_length() + 7) // 8, 'big'
            ),
        )
        expected = (
            "9MA8fRQrT4u8Zj8ZRd6MAiiyaxb2Y1CMpvVkHQu5hVM6",
            "4fE3H2E6XMp4SsxtwinF7w9a34ooUrwWe4WsW1458Pd",
            "EQJsjkd6JaGwxrjEhfeqPenqHwrBmPQZjJGNSCHBkcF7",
        )

        for i, hex_value in enumerate(testcases):
            result = encode_base58(hex_value)
            self.assertEqual(result, expected[i])
