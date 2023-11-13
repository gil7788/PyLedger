import unittest
from EllipticCurvePoint import EllipticCurvePoint
from ModuloPrimeGroup import ModuloPrimeGroup


class TestEllipticCurvePointCurve1(unittest.TestCase):
    # Tests for curve, e.g., y^2 = x^3 + 5x + 7
    def setUp(self):
        self.a, self.b = 5, 7
        # Define specific points for this curve
        self.P = EllipticCurvePoint(18, 77, self.a, self.b)
        self.Q = EllipticCurvePoint(2, -5, self.a, self.b)

    # Define test methods for curve y^2 = x^3 + 5x + 7
    def test_point_addition_new_polynom(self):
        R = self.P + self.Q
        x_r = 6.265625
        y_r = -16.861328125
        self.assertEqual(R, EllipticCurvePoint(x_r, y_r, self.a, self.b))

    def test_point_scalar_multiplication(self):
        R = 7 * self.P
        expected = self.P + self.P + self.P + self.P + self.P + self.P + self.P
        self.assertEqual(R, expected)


class TestEllipticCurvePointCurve2(unittest.TestCase):
    def setUp(self):
        # Common setup for the tests
        self.a, self.b = 2, 3  # Example curve coefficients y^2 = x^3 + ax + b
        self.P = EllipticCurvePoint(3, 6, self.a, self.b)  # A point on the curve
        self.Q = EllipticCurvePoint(-1, 0, self.a, self.b)  # Another point on the curve
        self.infinity = EllipticCurvePoint(None, None, self.a, self.b)  # Point at infinity

    def test_point_on_curve(self):
        # Point on the curve
        self.assertTrue(self.P.is_on_curve())
        # Point not on the curve
        with self.assertRaises(ValueError):
            EllipticCurvePoint(2, 3, self.a, self.b)

    def test_point_addition(self):
        # Test P + Q
        R = self.P + self.Q
        self.assertTrue(R.is_on_curve())

        # Test P + P (point doubling)
        R = self.P + self.P
        self.assertTrue(R.is_on_curve())

    def test_point_addition_equal_x(self):
        p = EllipticCurvePoint(3, 6, self.a, self.b)
        q = EllipticCurvePoint(3, -6, self.a, self.b)
        R = p + q
        self.assertEqual(R, self.infinity)

    def test_point_addition_same_point(self):
        p = EllipticCurvePoint(3, 6, self.a, self.b)
        q = EllipticCurvePoint(3, 6, self.a, self.b)
        R = p + q
        self.assertEqual(R, EllipticCurvePoint(-0.1597222222222232, 1.635995370370372, self.a, self.b))

    def test_point_addition_same_point_y_0(self):
        p = EllipticCurvePoint(-1, 0, self.a, self.b)
        q = EllipticCurvePoint(-1, 0, self.a, self.b)
        R = p + q
        self.assertEqual(R, self.infinity)

    def test_point_addition_negative_slope(self):
        p = EllipticCurvePoint(-1, 0, self.a, self.b)
        q = EllipticCurvePoint(3, -6, self.a, self.b)
        R = p + q
        self.assertEqual(R, EllipticCurvePoint(0.25, 1.875, self.a, self.b))

    def test_addition_with_infinity(self):
        # Test P + 0 (where 0 is the point at infinity)
        R = self.P + self.infinity
        self.assertEqual(R, self.P)

        # Test 0 + P
        R = self.infinity + self.P
        self.assertEqual(R, self.P)

    def test_point_negation(self):
        # Test P + (-P)
        negP = EllipticCurvePoint(self.P.x, -self.P.y, self.a, self.b)
        R = self.P + negP
        self.assertEqual(R, self.infinity)

    def test_equality_and_inequality(self):
        # Test equality
        self.assertEqual(self.P, EllipticCurvePoint(3, 6, self.a, self.b))

        # Test inequality
        self.assertNotEqual(self.P, self.Q)

    def test_repr(self):
        # Test the string representation of a point
        self.assertEqual(str(self.P), "EllipticCurvePoint(3, 6) on curve y^2 = x^3 + 2x + 3")


class TestFinalFieldEllipticCurvePoint(unittest.TestCase):
    def setUp(self):
        # Common setup for the tests
        self.prime = 17
        self.a = ModuloPrimeGroup(2, prime=self.prime)
        self.b = ModuloPrimeGroup(3, prime=self.prime)
        self.Px = ModuloPrimeGroup(3, prime=self.prime)
        self.Py = ModuloPrimeGroup(6, prime=self.prime)
        self.Qx = ModuloPrimeGroup(-1, prime=self.prime)
        self.Qy = ModuloPrimeGroup(0, prime=self.prime)

        self.P = EllipticCurvePoint(self.Px, self.Py, self.a, self.b)  # A point on the curve
        self.Q = EllipticCurvePoint(self.Qx, self.Qy, self.a, self.b)  # Another point on the curve
        self.infinity = EllipticCurvePoint(None, None, self.a, self.b)  # Point at infinity

    def test_point_on_curve(self):
        # Point on the curve
        self.assertTrue(self.P.is_on_curve())
        # Point not on the curve
        with self.assertRaises(ValueError):
            p_x = ModuloPrimeGroup(2, prime=self.prime)
            p_y = ModuloPrimeGroup(3, prime=self.prime)
            EllipticCurvePoint(p_x, p_y, self.a, self.b)

    def test_point_addition(self):
        # Test P + Q
        R = self.P + self.Q
        self.assertTrue(R.is_on_curve())

        # Test P + P (point doubling)
        R = self.P + self.P
        self.assertTrue(R.is_on_curve())

    def test_point_addition_equal_x(self):
        p = EllipticCurvePoint(self.Px, self.Py, self.a, self.b)
        q = EllipticCurvePoint(self.Px, -self.Py, self.a, self.b)
        R = p + q
        self.assertEqual(R, self.infinity)

    def test_point_addition_same_point(self):
        p = EllipticCurvePoint(self.Px, self.Py, self.a, self.b)
        q = EllipticCurvePoint(self.Px, self.Py, self.a, self.b)
        R = p + q
        expected_x = ModuloPrimeGroup(12, prime=self.prime)
        expected_y = ModuloPrimeGroup(2, prime=self.prime)
        self.assertEqual(R, EllipticCurvePoint(expected_x, expected_y, self.a, self.b))

    def test_point_addition_same_point_y_0(self):
        p_x = ModuloPrimeGroup(-1, prime=self.prime)
        p_y = ModuloPrimeGroup(0, prime=self.prime)
        p = EllipticCurvePoint(p_x, p_y, self.a, self.b)
        q = EllipticCurvePoint(p_x, p_y, self.a, self.b)
        R = p + q
        self.assertEqual(R, self.infinity)

    def test_point_addition_negative_slope(self):
        p_x = ModuloPrimeGroup(-1, prime=self.prime)
        p_y = ModuloPrimeGroup(0, prime=self.prime)
        p = EllipticCurvePoint(p_x, p_y, self.a, self.b)
        q_y = ModuloPrimeGroup(-6, prime=self.prime)

        q = EllipticCurvePoint(self.Px, q_y, self.a, self.b)
        R = p + q
        expected_x = ModuloPrimeGroup(13, prime=self.prime)
        expected_y = ModuloPrimeGroup(4, prime=self.prime)

        self.assertEqual(R, EllipticCurvePoint(expected_x, expected_y, self.a, self.b))

    def test_addition_with_infinity(self):
        # Test P + 0 (where 0 is the point at infinity)
        R = self.P + self.infinity
        self.assertEqual(R, self.P)

        # Test 0 + P
        R = self.infinity + self.P
        self.assertEqual(R, self.P)

    def test_point_negation(self):
        # Test P + (-P)
        negP = EllipticCurvePoint(self.Px, -self.Py, self.a, self.b)
        R = self.P + negP
        self.assertEqual(R, self.infinity)

    def test_equality_and_inequality(self):
        # Test equality
        self.assertEqual(self.P, self.P)

        # Test inequality
        self.assertNotEqual(self.P, self.Q)


if __name__ == '__main__':
    unittest.main()
