import unittest
from random import randint
import src.sha256.secp256k1_config as secp
from src.PrivateKey import PrivateKey
from src.utils.encoding_utils import little_endian_to_int, hash256


class TestPrivateKey(unittest.TestCase):
    def test_sign(self):
        pk = PrivateKey(randint(0, secp.N))
        z = randint(0, 2 ** 256)
        sig = pk.sign(z)
        self.assertTrue(pk.point.verify(z, sig))

    def test_wif(self):
        pk = PrivateKey(2 ** 256 - 2 ** 199)
        expected = 'L5oLkpV3aqBJ4BgssVAsax1iRa77G5CVYnv9adQ6Z87te7TyUdSC'
        self.assertEqual(pk.wif(compressed=True, testnet=False), expected)
        pk = PrivateKey(2 ** 256 - 2 ** 201)
        expected = '93XfLeifX7Jx7n7ELGMAf1SUR6f9kgQs8Xke8WStMwUtrDucMzn'
        self.assertEqual(pk.wif(compressed=False, testnet=True), expected)
        pk = PrivateKey(0x0dba685b4511dbd3d368e5c4358a1277de9486447af7b3604a69b8d9d8b7889d)
        expected = '5HvLFPDVgFZRK9cd4C5jcWki5Skz6fmKqi1GQJf5ZoMofid2Dty'
        self.assertEqual(pk.wif(compressed=False, testnet=False), expected)
        pk = PrivateKey(0x1cca23de92fd1862fb5b76e5f4f50eb082165e5191e116c18ed1a6b24be6a53f)
        expected = 'cNYfWuhDpbNM1JWc3c6JTrtrFVxU4AGhUKgw5f93NP2QaBqmxKkg'
        self.assertEqual(pk.wif(compressed=True, testnet=True), expected)

    def test_wif_public_key(self):
        testcases = (
            (5003, True, True),
            (pow(2021, 5), False, True),
            (0x54321deadbeef, True, False)
        )
        expected = (
            "cMahea7zqjxrtgAbB7LSGbcQUr1uX1ojuat9jZodMN8rFTv2sfUK",
            "91avARGdfge8E4tZfYLoxeJ5sGBdNJQH4kvjpWAxgzczjbCwxic",
            "KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgiuQJv1h8Ytr2S53a"
        )

        for i, v in enumerate(testcases):
            pk = PrivateKey(v[0])
            result = pk.wif(compressed=v[1], testnet=v[2])
            self.assertEqual(expected[i], result)

    def test_generate_testnet_address(self):
        passphrase = b'jimmy@programmingblockchain.com my secret'
        hashed_passphrase = hash256(passphrase)
        secret = little_endian_to_int(hashed_passphrase)
        pk = PrivateKey(secret)
        result = pk.point.address(compressed=True, testnet=True)
        expected_from_book = "mft9LRNtaBNtpkknB8xgm17UvPedZ4ecYL"
        expected ="7pwS2XAt25Rdc8J9vfB31Q1LbzqWH"
        self.assertEqual(expected, result)
