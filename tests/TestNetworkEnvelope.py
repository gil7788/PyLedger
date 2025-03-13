import unittest
from io import BytesIO

from src.NetworkEnvelope import NetworkEnvelope


class MyTestCase(unittest.TestCase):
    def test_something(self):
        ne = NetworkEnvelope.parse(BytesIO(bytes.fromhex("f9beb4d976657261636b000000000000000000005df6e0e2")), False)

        self.assertIsInstance(ne, NetworkEnvelope)
        self.assertEqual(b'verack', ne.command)
        self.assertEqual(b'', ne.payload)


if __name__ == '__main__':
    unittest.main()
