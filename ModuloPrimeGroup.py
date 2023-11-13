class ModuloPrimeGroup:
    def __init__(self, value, prime):
        if isinstance(value, ModuloPrimeGroup):
            value = value.value
        self.value = value % prime
        self.prime = prime

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.subtract(other)

    def __mul__(self, other):
        return self.multiply(other)

    def __pow__(self, exponent):
        return self.exponentiation(exponent)

    def __truediv__(self, other):
        return self.divide(other)

    def __eq__(self, other):
        return self.value == other.value and self.prime == other.prime

    def __ne__(self, other):
        return not (self == other)

    def __neg__(self):
        return ModuloPrimeGroup(-self.value, self.prime)

    def __rmul__(self, coefficient):
        return self.__class__(coefficient * self.value, self.prime)

    def add(self, other):
        if self.prime != other.prime:
            raise ValueError("Operands must be in the same modulo prime group.")
        return ModuloPrimeGroup((self.value + other.value) % self.prime, self.prime)

    def subtract(self, other):
        if self.prime != other.prime:
            raise ValueError("Operands must be in the same modulo prime group.")
        return ModuloPrimeGroup((self.value - other.value) % self.prime, self.prime)

    def multiply(self, other):
        if self.prime != other.prime:
            raise ValueError("Operands must be in the same modulo prime group.")
        return ModuloPrimeGroup((self.value * other.value) % self.prime, self.prime)

    def exponentiation(self, exponent):
        return ModuloPrimeGroup(pow(self.value, exponent, self.prime), self.prime)

    def inverse(self):
        # Using Fermat's Little Theorem for finding the multiplicative inverse
        return ModuloPrimeGroup(pow(self.value, self.prime - 2, self.prime), self.prime)

    def divide(self, other):
        if self.prime != other.prime:
            raise ValueError("Operands must be in the same modulo prime group.")
        return self.multiply(other.inverse())

    def __str__(self):
        return f"Value: {self.value} in Z_{self.prime}"

    def __repr__(self):
        return f"Value: {self.value} in Z_{self.prime}"
