import unittest
from random import randint

from src.Signature import Signature


class TestSignature(unittest.TestCase):
    def test_der(self):
        testcases = (
            (1, 2),
            (randint(0, 2 ** 256), randint(0, 2 ** 255)),
            (randint(0, 2 ** 256), randint(0, 2 ** 255)),
        )
        for r, s in testcases:
            sig = Signature(r, s)
            der = sig.der()
            sig2 = Signature.parse(der)
            self.assertEqual(sig2.r, r)
            self.assertEqual(sig2.s, s)

    def test_specific_der(self):
        self.assertEqual(0,0)
        r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
        s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
        #
        sig = Signature(r, s)
        der = sig.der()

        # validate that decoding works well
        sig2 = Signature.parse(der)

        self.assertEqual(der.hex(), "3045022037206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6022100\
8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec")
