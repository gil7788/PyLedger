class ModuloPrimeGroup:
    def __init__(self, value, prime):
        if not self.is_prime(prime):
            raise ValueError("Prime must be a prime number.")
        self.value = value % prime
        self.prime = prime

    @staticmethod
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

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

    def exponentiate(self, exponent):
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
