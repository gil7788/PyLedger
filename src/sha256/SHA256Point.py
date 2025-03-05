from src.EllipticCurvePoint import EllipticCurvePoint
from src.sha256.SHA256Element import SHA256Element
import src.sha256.secp256k1_config as secp
from src.utils.encoding_utils import hash160,encode_base58


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

    def address(self, compressed=True, testnet=False):
        address = self.sec_hash160(compressed)

        if testnet:
            prefix = b"\x6f"  # Correct testnet prefix for Bitcoin addresses
        else:
            prefix = b"\x00"  # Correct mainnet prefix for Bitcoin addresses

        return encode_base58(prefix + address)  # Now prefix is bytes, no TypeError

    def sec_hash160(self, compressed=True):
        return hash160(self.sec(compressed))

    def sec(self, compressed=True):
        # returns the binary version of the SEC format
        if compressed:
            if self.y.value % 2 == 0:
                return b'\x02' + self.x.value.to_bytes(32, 'big')
            else:
                return b'\x03' + self.x.value.to_bytes(32, 'big')
        else:
            return b'\x04' + self.x.value.to_bytes(32, 'big') + self.y.value.to_bytes(32, 'big')

    @classmethod
    def parse(cls, sec_bin):
        if sec_bin[0] == 4:
            x = int.from_bytes(sec_bin[1:33], 'big')
            y = int.from_bytes(sec_bin[33:65], 'big')
            return SHA256Point(x, y)
        is_even = sec_bin[0] == 2
        x = SHA256Element(int.from_bytes(sec_bin[1:], 'big'))
        alpha = x**3 + SHA256Element(secp.A) * x + SHA256Element(secp.B)
        beta = alpha.sqrt()
        if beta.value % 2 == 0:
            even_beta = beta
            odd_beta = SHA256Element(secp.PRIME - beta.value)
        else:
            even_beta = SHA256Element(secp.PRIME - beta.value)
            odd_beta = beta
        if is_even:
            return SHA256Point(x, even_beta)
        else:
            return SHA256Point(x, odd_beta)

    def __rmul__(self, coefficient):
        elliptic_curve_point = super().__rmul__(coefficient)
        return SHA256Point(elliptic_curve_point.x, elliptic_curve_point.y)

    def __repr__(self):
        if self.x is None:
            return 'S256Point(infinity)'
        else:
            return 'S256Point({}, {})'.format(self.x, self.y)
