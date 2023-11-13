from src.ModuloGroup import ModuloGroup
import src.sha256.secp256k1_config as secp


class SHA256Element(ModuloGroup):
    def __init__(self, value, prime=secp.PRIME):
        super().__init__(value, prime=prime)

    def sqrt(self):
        # returns the square root mod p, hold for p = 3 mod 4, including secp256k1
        return self.__pow__((self.prime + 1) // 4)

    def __add__(self, other):
        result = super().__add__(other)
        return SHA256Element(result.value, self.prime)

    def __sub__(self, other):
        result = super().__sub__(other)
        return SHA256Element(result.value, self.prime)

    def __mul__(self, other):
        result = super().__mul__(other)
        return SHA256Element(result.value, self.prime)

    def __pow__(self, exponent):
        result = super().__pow__(exponent)
        return SHA256Element(result.value, self.prime)

    def __truediv__(self, other):
        result = super().__truediv__(other)
        return SHA256Element(result.value, self.prime)

    def __neg__(self):
        result = super().__neg__()
        return SHA256Element(result.value, self.prime)

    def __rmul__(self, coefficient):
        result = super().__rmul__(coefficient)
        return SHA256Element(result.value, self.prime)

    def __eq__(self, other):
        return super().__eq__(other)

    def __ne__(self, other):
        return super().__ne__(other)

    def __repr__(self):
        return '{:x}'.format(self.value).zfill(64)
