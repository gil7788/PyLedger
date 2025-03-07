from src.tx.TxIn import TxIn
from src.tx.TxOut import TxOut
from src.utils.encoding_utils import little_endian_to_int, int_to_little_endian, read_varint, encode_varint


class Tx:
    def __init__(self, version, testnet, tx_ins, tx_outs, locktime):
        self.version = version
        self.testnet = testnet
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime

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
