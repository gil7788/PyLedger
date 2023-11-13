import unittest

from ModuloGroup import ModuloGroup


class TestModuloGroup(unittest.TestCase):
    def test_equality(self):
        a = ModuloGroup(3, 7)
        b = ModuloGroup(3, 7)
        self.assertEqual(a, b)

    def test_inequality(self):
        a = ModuloGroup(3, 7)
        b = ModuloGroup(4, 7)
        self.assertNotEqual(a, b)

    def test_negation(self):
        a = ModuloGroup(3, 7)
        self.assertEqual(-a, ModuloGroup(4, 7))

    def test_rmul(self):
        a = ModuloGroup(3, 7)
        self.assertEqual(2 * a, ModuloGroup(6, 7))

    def test_modulo_operation(self):
        mp = ModuloGroup(10, 7)
        self.assertEqual(mp.value, 3)  # 10 mod 7

    def test_addition(self):
        a = ModuloGroup(3, 7)
        b = ModuloGroup(5, 7)
        self.assertEqual((a + b).value, 1)  # (3 + 5) mod 7

    def test_subtraction(self):
        a = ModuloGroup(3, 7)
        b = ModuloGroup(5, 7)
        self.assertEqual((a - b).value, 5)  # (3 - 5) mod 7

    def test_multiplication(self):
        a = ModuloGroup(3, 7)
        b = ModuloGroup(5, 7)
        self.assertEqual((a * b).value, 1)  # (3 * 5) mod 7

    def test_division(self):
        a = ModuloGroup(3, 7)
        b = ModuloGroup(5, 7)
        self.assertEqual((a / b).value, 2)  # (3 / 5) mod 7

    def test_exponentiation(self):
        a = ModuloGroup(3, 7)
        self.assertEqual((a ** 2).value, 2)  # (3^2) mod 7

    def test_inverse(self):
        a = ModuloGroup(3, 7)
        self.assertEqual(a.inverse().value, 5)  # 3 * 5 mod 7 = 1

    def test_different_primes(self):
        a = ModuloGroup(2, 7)
        b = ModuloGroup(3, 11)
        with self.assertRaises(ValueError):
            a + b
        with self.assertRaises(ValueError):
            a - b
        with self.assertRaises(ValueError):
            a * b
        with self.assertRaises(ValueError):
            a / b

    def test_coefficient_multiplication(self):
        a = ModuloGroup(3, 7)
        self.assertEqual((2 * a).value, 6)

    def test_repr(self):
        a = ModuloGroup(3, 7)
        self.assertEqual(str(a), "Value: 3 in Z_7")


if __name__ == '__main__':
    unittest.main()
