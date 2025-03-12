from src.utils.encoding_utils import (
    little_endian_to_int,
    int_to_little_endian,
    read_varint,
    encode_varint,
    hash256,
    SIGHASH_ALL
)
from src.tx.Script import Script

from io import BytesIO
import requests


class Tx:
    def __init__(self, version, testnet, tx_ins, tx_outs, locktime):
        self.version = version
        self.testnet = testnet
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime

    def sign_input(self, input_index, private_key):
        z = self.sig_hash(input_index)

        der = private_key.sign(z).der()
        sig = der + SIGHASH_ALL.to_bytes(1, 'big')
        sec = private_key.point.sec()
        self.tx_ins[input_index].script_sig = Script([sig, sec])
        return self.verify_input(input_index)

    def verify(self):
        '''Verify this transaction'''

        if self.fee() < 0:
            return False
        for i in range(len(self.tx_ins)):
            if not self.verify_input(i):
                return False
        return True

    def verify_input(self, input_index):
        tx_in = self.tx_ins[input_index]

        script_pubkey = tx_in.script_pubkey(testnet=self.testnet)
        z = self.sig_hash(input_index)
        combined = tx_in.script_sig + script_pubkey
        return combined.evaluate(z)

    def sig_hash(self, input_index):
        s = int_to_little_endian(self.version, 4)

        s += encode_varint(len(self.tx_ins))
        for i, tx_in in enumerate(self.tx_ins):

            if i == input_index:
                s += TxIn(
                    prev_tx=tx_in.prev_tx,
                    prev_index=tx_in.prev_index,
                    script_sig=tx_in.script_pubkey(self.testnet),
                    sequence=tx_in.sequence,
                ).serialize()
            else:
                s += TxIn(
                    prev_tx=tx_in.prev_tx,
                    prev_index=tx_in.prev_index,
                    sequence=tx_in.sequence,
                ).serialize()
            s += encode_varint(len(self.tx_outs))
            for tx_out in self.tx_outs:
                s += tx_out.serialize()
            s += int_to_little_endian(self.locktime, 4)
            s += int_to_little_endian(SIGHASH_ALL, 4)
            h256 = hash256(s)
            return int.from_bytes(h256, 'big')

    def fee(self, testnet=False):
        input_sum, output_sum = 0, 0

        for tx_in in self.tx_ins:
            input_sum += tx_in.value(testnet=testnet)
        for tx_out in self.tx_outs:
            output_sum += tx_out.amount
        return input_sum - output_sum

    @classmethod
    def parse(cls, tx_bytes, testnet=False):
        version = little_endian_to_int(tx_bytes.read(4))

        number_of_ins = read_varint(tx_bytes)
        ins = []
        for _ in range(number_of_ins):
            ins.append(TxIn.parse(tx_bytes))

        number_of_outs = read_varint(tx_bytes)
        outs = []
        for _ in range(number_of_outs):
            outs.append(TxOut.parse(tx_bytes))

        locktime = little_endian_to_int(tx_bytes.read(4))
        return cls(version,testnet, ins, outs, locktime)

    def serialize(self):
        result = int_to_little_endian(self.version, 4)
        result += encode_varint(len(self.tx_ins))
        for tx_in in self.tx_ins:
            result += tx_in.serialize()
        result += encode_varint(len(self.tx_outs))
        for tx_out in self.tx_outs:
            result += tx_out.serialize()
        result += int_to_little_endian(self.locktime, 4)
        return result


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


class TxFetcher:
    cache = {}

    @classmethod
    def get_url(cls, testnet=False):
        if testnet:
            return 'http://testnet.programmingbitcoin.com'
        else:
            return 'http://mainnet.programmingbitcoin.com'

    @classmethod
    def fetch(cls, tx_id, testnet=False, fresh=False):
        if fresh or (tx_id not in cls.cache):
            url = '{}/tx/{}.hex'.format(cls.get_url(testnet), tx_id)
            response = requests.get(url)
            try:
                raw = bytes.fromhex(response.text.strip())
            except ValueError:
                raise ValueError('unexpected response: {}'.format(response.text))

            if raw[4] == 0:
                raw = raw[:4] + raw[6:]
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
                tx.locktime = little_endian_to_int(raw[-4:])
            else:
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
            if tx.id() != tx_id:
                raise ValueError('not the same id: {} vs {}'.format(tx.id(), tx_id))

            cls.cache[tx_id] = tx

        cls.cache[tx_id].testnet = testnet
        return cls.cache[tx_id]


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