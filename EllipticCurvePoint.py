import logging

from ModuloPrimeGroup import ModuloPrimeGroup


class EllipticCurvePoint:
    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b

        # Handling the point at infinity.
        if self.is_zero():
            return

        # Ensuring the point lies on the elliptic curve.
        if not self.is_on_curve():
            raise ValueError(f"The point ({x}, {y}) is not on the curve y^2 = x^3 + {a}x + {b}.")

    def is_zero(self):
        return self.x is None and self.y is None

    def is_on_curve(self, tolerance=1e-10):
        if self.is_zero():
            return True

        if isinstance(self.x, ModuloPrimeGroup) and isinstance(self.y, ModuloPrimeGroup):
            return self.y ** 2 == self.x ** 3 + self.a * self.x + self.b
        else:
            return abs(self.y**2 - (self.x**3 + self.a * self.x + self.b)) < tolerance

    def __eq__(self, other, tolerance=1e-10):
        if self.is_zero():
            return other.is_zero()

        if isinstance(self.x, ModuloPrimeGroup) and isinstance(other.x, ModuloPrimeGroup):
            return self.x == other.x and self.y == other.y
        else:
            return (abs(self.x - other.x) < tolerance) and (abs(self.y - other.y) < tolerance)

    def __ne__(self, other):
        return not (self == other)

    def __neg__(self):
        # If the point is at infinity, return it as is
        if self.is_zero():
            return self

        # For a regular point, negate the y coordinate
        return self.__class__(self.x, -self.y, self.a, self.b)

    def __rmul__(self, coefficient):
        return self.binary_exponentiation(coefficient)

    def binary_exponentiation(self, exponent):
        result = self.__class__(None, None, self.a, self.b)
        print(len(bin(exponent)[2:]))
        i = 0
        for bit in bin(exponent)[2:]:
            print(i)
            i+=1
            result += result
            if bit == "1":
                result += self
        return result

    def __add__(self, other):
        if (self.a, self.b) != (other.a, other.b):
            raise TypeError("Points are not on the same curve.")

        # Adding with the point at infinity.
        if self.is_zero():
            return other
        if other.is_zero():
            return self

        # Handling the case of P + (-P) = 0.
        if self.x == other.x and self.y != other.y:
            return EllipticCurvePoint(None, None, self.a, self.b)

        if self.x != other.x:
            slope = (other.y - self.y) / (other.x - self.x)
            x3 = slope**2 - self.x - other.x
            y3 = slope * (self.x - x3) - self.y
            return EllipticCurvePoint(x3, y3, self.a, self.b)

        if self == other:
            # Point doubling, handling the case of vertical tangent line.
            if self.y == self._ensure_same_type(0):
                return EllipticCurvePoint(None, None, self.a, self.b)
            slope = (3 * self.x**2 + self.a) / (2 * self.y)
            x3 = slope**2 - 2 * self.x
            y3 = slope * (self.x - x3) - self.y
            return EllipticCurvePoint(x3, y3, self.a, self.b)

        logging.error("Unexpected case in EllipticCurvePoint addition: adding {} and {}".format(self, other))
        raise ValueError("Unexpected case in EllipticCurvePoint addition: adding {} and {}".format(self, other))

    def _ensure_same_type(self, value):
        """
        Ensure that the value is of the same type as the curve parameters.
        """
        if isinstance(value, int) and (isinstance(self.x, ModuloPrimeGroup) or isinstance(self.y, ModuloPrimeGroup)):
            return ModuloPrimeGroup(value, self.x.prime)  # Assuming self.x and self.y have the same prime
        return value

    @staticmethod
    def _is_equal_to_zero(value):
        """
        Check if a value (either int or ModuloPrimeGroup) is equal to zero.
        """
        if isinstance(value, ModuloPrimeGroup):
            return value.value == 0
        return value == 0

    def __repr__(self):
        if self.is_zero():
            return "Point at infinity"
        return f"EllipticCurvePoint({self.x}, {self.y}) on curve y^2 = x^3 + {self.a}x + {self.b}"
