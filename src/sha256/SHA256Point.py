from src.EllipticCurvePoint import EllipticCurvePoint
from src.sha256.SHA256Element import SHA256Element
import src.sha256.secp256k1_config as secp


class SHA256Point(EllipticCurvePoint):
    def __init__(self, x, y, a=secp.A, b=secp.B):
        if isinstance(a, int):
            a = SHA256Element(a)
        if isinstance(b, int):
            b = SHA256Element(b)
        if isinstance(x, int):
            x = SHA256Element(x)
        if isinstance(y, int):
            y = SHA256Element(y)
        super().__init__(x=x, y=y, a=a, b=b)

    @staticmethod
    def get_g():
        gx_element = SHA256Element(secp.Gx, prime=secp.PRIME)
        gy_element = SHA256Element(secp.Gy, prime=secp.PRIME)
        return SHA256Point(gx_element, gy_element)

    def verify(self, z, sig):
        s_inv = pow(sig.s, secp.N - 2, secp.N)
        u = z * s_inv % secp.N
        v = sig.r * s_inv % secp.N
        total = u * self.get_g() + v * self
        return total.x.value == sig.r

    def __rmul__(self, coefficient):
        coefficient = coefficient % secp.N
        return super().__rmul__(coefficient)

    def __repr__(self):
        if self.x is None:
            return 'S256Point(infinity)'
        else:
            return 'S256Point({}, {})'.format(self.x, self.y)
