import hashlib
import hmac

from src.utils.encoding_utils import encode_base58_checksum
from src.sha256 import secp256k1_config as secp


from src.sha256.SHA256Point import SHA256Point
from src.Signature import Signature


class PrivateKey:
    def __init__(self, secret):
        self.secret = secret
        self.point = secret * SHA256Point.get_g()

    def sign(self, z):
        k = self.deterministic_k(z)

        r = (k * SHA256Point.get_g()).x.value
        k_inv = pow(k, secp.N - 2, secp.N)
        s = (z + r * self.secret) * k_inv % secp.N
        if s > secp.N / 2:
            s = secp.N - s
        return Signature(r, s)

    def deterministic_k(self, z):
        k = b'\x00' * 32

        v = b'\x01' * 32
        if z > secp.N:
            z -= secp.N
        z_bytes = z.to_bytes(32, 'big')
        secret_bytes = self.secret.to_bytes(32, 'big')
        s256 = hashlib.sha256
        k = hmac.new(k, v + b'\x00' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b'\x01' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while True:
            v = hmac.new(k, v, s256).digest()
            candidate = int.from_bytes(v, 'big')

            if candidate >= 1 and candidate < secp.N:
                return candidate
            k = hmac.new(k, v + b'\x00', s256).digest()
            v = hmac.new(k, v, s256).digest()

    def wif(self, compressed=True, testnet=False):
        secret_bytes = self.secret.to_bytes(32, 'big')
        if testnet:
            prefix = b'\xef'
        else:
            prefix = b'\x80'
        if compressed:
            suffix = b'\x01'
        else:
            suffix = b''
        return encode_base58_checksum(prefix + secret_bytes + suffix)

    def hex(self):
        return '{:x}'.format(self.secret).zfill(64)
