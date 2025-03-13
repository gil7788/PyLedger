from src.utils.encoding_utils import little_endian_to_int, hash256, int_to_little_endian

NETWORK_MAGIC = b'\xf9\xbe\xb4\xd9'
TESTNET_NETWORK_MAGIC = b'\x0b\x11\x09\x07'


class NetworkEnvelope:
    def __init__(self, command, payload, testnet=False):
        self.command = command
        self.payload = payload
        if testnet:
            self.magic = TESTNET_NETWORK_MAGIC
        else:
            self.magic = NETWORK_MAGIC

    def serialize(self):
        missing_bytes = (12 - len(self.command))
        command = missing_bytes * b'\x00' + self.command
        payload_len = int_to_little_endian(len(self.payload), 4)
        checksum = hash256(self.payload)[:4]
        strs = [self.magic, command, payload_len, checksum, self.payload]
        return ''.join(strs)

    @classmethod
    def parse(cls, stream, testnet=False):
        magic = stream.read(4)

        if magic == b'':
            raise IOError('Connection reset!')
        if testnet:
            expected_magic = TESTNET_NETWORK_MAGIC
        else:
            expected_magic = NETWORK_MAGIC
        if magic != expected_magic:
            raise SyntaxError('magic is not right {} vs {}'.format(magic.hex(),
                                                                   expected_magic.hex()))
        command = stream.read(12)
        command = command.strip(b'\x00')
        payload_length = little_endian_to_int(stream.read(4))
        payload_checksum = stream.read(4)
        payload = stream.read(payload_length)
        if not hash256(payload)[:4] == payload_checksum:
            raise IOError('checksum does not match')

        return cls(command, payload, testnet)

    def __repr__(self):
        return '{}: {}'.format(
            self.command.decode('ascii'),
            self.payload.hex(),
        )
