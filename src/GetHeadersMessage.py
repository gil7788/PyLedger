from src.utils.encoding_utils import int_to_little_endian, encode_varint


class GetHeadersMessage:
    command = b'getheaders'

    def __init__(self, version=70015, num_hashes=1, start_block=None, end_block=None):
        self.version = version
        self.num_hashes = num_hashes

        if start_block is None:
            raise RuntimeError('a start block is required')
        self.start_block = start_block
        if end_block is None:
            self.end_block = b'\x00' * 32
        else:
            self.end_block = end_block

    def serialize(self):
        version = int_to_little_endian(self.version, 4)
        num_hashes = encode_varint(self.num_hashes)
        strs = [version, num_hashes, self.start_block[::-1], self.end_block[::-1]]
        return ''.join(strs)