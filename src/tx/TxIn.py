from src.tx.Script import Script
from src.tx.TxFetcher import TxFetcher
from src.utils.encoding_utils import little_endian_to_int, int_to_little_endian


class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig = None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if not script_sig:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence

    def fetch_tx(self, testnet=False):
        return TxFetcher.fetch(self.prev_tx.hex(), testnet=testnet)

    def value(self, testnet=False):
        '''
        Get the output value by looking up the tx hash. Returns the amount in satoshi.
        '''
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].amount

    def script_pubkey(self, testnet=False):
        '''Get the ScriptPubKey by looking up the tx hash.
        Returns a Script object.
        '''

        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].script_pubkey

    def serialize(self):
        '''Returns the byte serialization of the transaction input'''

        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += int_to_little_endian(self.sequence, 4)
        return result

    @classmethod
    def parse(cls, s):
        '''Takes a byte stream and parses the tx_input at the start.
        Returns a TxIn object.
        '''

        prev_tx = s.read(32)[::-1]
        prev_index = little_endian_to_int(s.read(4))
        script_sig = Script.parse(s)
        sequence = little_endian_to_int(s.read(4))
        return cls(prev_tx, prev_index, script_sig, sequence)

    def __repr__(self):
        return '{}:{}'.format(
            self.prev_tx.hex(),
            self.prev_index,
        )