from ModuloGroup import ModuloGroup
import secp256k1_config as secp


class SHA256Element(ModuloGroup):
    def __init__(self, value, prime=secp.PRIME):
        super().__init__(value, prime=prime)
        self.value = value

    def __repr__(self):
        return '{:x}'.format(self.value).zfill(64)
