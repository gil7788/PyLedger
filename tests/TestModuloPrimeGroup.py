import unittest

from ModuloPrimeGroup import ModuloPrimeGroup


class TestModuloPrimeGroup(unittest.TestCase):
    def test_equality(self):
        a = ModuloPrimeGroup(3, 7)
        b = ModuloPrimeGroup(3, 7)
        self.assertEqual(a, b)

    def test_inequality(self):
        a = ModuloPrimeGroup(3, 7)
        b = ModuloPrimeGroup(4, 7)
        self.assertNotEqual(a, b)

    def test_negation(self):
        a = ModuloPrimeGroup(3, 7)
        self.assertEqual(-a, ModuloPrimeGroup(4, 7))

    def test_rmul(self):
        a = ModuloPrimeGroup(3, 7)
        self.assertEqual(2 * a, ModuloPrimeGroup(6, 7))

    def test_modulo_operation(self):
        mp = ModuloPrimeGroup(10, 7)
        self.assertEqual(mp.value, 3)  # 10 mod 7

    def test_addition(self):
        a = ModuloPrimeGroup(3, 7)
        b = ModuloPrimeGroup(5, 7)
        self.assertEqual((a + b).value, 1)  # (3 + 5) mod 7

    def test_subtraction(self):
        a = ModuloPrimeGroup(3, 7)
        b = ModuloPrimeGroup(5, 7)
        self.assertEqual((a - b).value, 5)  # (3 - 5) mod 7

    def test_multiplication(self):
        a = ModuloPrimeGroup(3, 7)
        b = ModuloPrimeGroup(5, 7)
        self.assertEqual((a * b).value, 1)  # (3 * 5) mod 7

    def test_division(self):
        a = ModuloPrimeGroup(3, 7)
        b = ModuloPrimeGroup(5, 7)
        self.assertEqual((a / b).value, 2)  # (3 / 5) mod 7

    def test_exponentiation(self):
        a = ModuloPrimeGroup(3, 7)
        self.assertEqual((a ** 2).value, 2)  # (3^2) mod 7

    def test_inverse(self):
        a = ModuloPrimeGroup(3, 7)
        self.assertEqual(a.inverse().value, 5)  # 3 * 5 mod 7 = 1

    def test_different_primes(self):
        a = ModuloPrimeGroup(2, 7)
        b = ModuloPrimeGroup(3, 11)
        with self.assertRaises(ValueError):
            a + b
        with self.assertRaises(ValueError):
            a - b
        with self.assertRaises(ValueError):
            a * b
        with self.assertRaises(ValueError):
            a / b

    def test_coefficient_multiplication(self):
        a = ModuloPrimeGroup(3, 7)
        self.assertEqual((2 * a).value, 6)

    def test_repr(self):
        a = ModuloPrimeGroup(3, 7)
        self.assertEqual(str(a), "Value: 3 in Z_7")


if __name__ == '__main__':
    unittest.main()
