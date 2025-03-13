from src.utils.encoding_utils import int_to_little_endian, little_endian_to_int, hash256, TWO_WEEKS
from io import BytesIO


class Block:
    def __init__(self, version, prev_block, merkle_root, timestamp, bits, nonce):
        self.version = version
        self.prev_block = prev_block
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = nonce

    def hash(self):
        pre_image = self.serialize()
        return hash256(pre_image)[::-1]

    def bip9(self):
        return self.version >> 29 == 0b100

    def bip91(self):
        return self.version >> 4 == 1

    def bip141(self):
        return self.version >> 1 == 1

    def check_pow(self):
        val = little_endian_to_int(hash256(self.serialize()))
        return val < self.target()

    def difficulty(self):
        target = self.target()
        return 0xffff * 256 ** (0x1d - 3) / target

    @staticmethod
    def bits_to_target(bits):
        exponent = bits[-1]
        coefficient = little_endian_to_int(bits[:-1])
        return coefficient * 256 ** (exponent - 3)

    def target(self):
        return Block.bits_to_target(self.bits)

    @classmethod
    def parse(cls, stream):
        version = little_endian_to_int(stream.read(4))
        prev_block = stream.read(32)[::-1]
        merkle_root = stream.read(32)[::-1]
        timestamp = little_endian_to_int(stream.read(4))
        bits = stream.read(4)
        nonce = stream.read(4)
        return cls(version, prev_block, merkle_root, timestamp, bits, nonce)

    def serialize(self):
        self_str = int_to_little_endian(self.version, 4)
        self_str += self.prev_block[::-1]
        self_str += self.merkle_root[::-1]
        self_str += int_to_little_endian(self.timestamp, 4)
        self_str += self.bits
        self_str += self.nonce
        return self_str


def calculate_new_block_bits(first_block_str, last_block_str):
    first_block = Block.parse(BytesIO(bytes.fromhex(first_block_str)))
    last_block = Block.parse(BytesIO(bytes.fromhex(last_block_str)))

    delta = last_block.timestamp - first_block.timestamp
    if delta > TWO_WEEKS * 4:
        delta = TWO_WEEKS * 4
    elif delta < TWO_WEEKS // 4:
        delta = TWO_WEEKS // 4

    new_target = last_block.target() * delta // TWO_WEEKS
    bits = target_to_bits(new_target)

    return bits.hex()


def target_to_bits(target):
    '''Turns a target integer back into bits'''
    raw_bytes = target.to_bytes(32, 'big')
    raw_bytes = raw_bytes.lstrip(b'\x00')
    if raw_bytes[0] > 0x7f:
        exponent = len(raw_bytes) + 1
        coefficient = b'\x00' + raw_bytes[:2]
    else:
        exponent = len(raw_bytes)
        coefficient = raw_bytes[:3]
    new_bits = coefficient[::-1] + bytes([exponent])
    return new_bits
