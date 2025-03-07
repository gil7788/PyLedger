from src.tx.Script import Script
from src.utils.encoding_utils import little_endian_to_int, int_to_little_endian


class TxOut:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def serialize(self):
        '''Returns the byte serialization of the transaction output'''

        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize()
        return result

    def __repr__(self):
        return '{}:{}'.format(self.amount, self.script_pubkey)

    @classmethod
    def parse(cls, s):
        '''Takes a byte stream and parses the tx_output at the start.
        Returns a TxOut object.
        '''
        amount = little_endian_to_int(s.read(8))
        script_pubkey = Script.parse(s)
        return cls(amount, script_pubkey)