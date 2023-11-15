from io import BytesIO


class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s

    def der(self):
        '''returns the byte serialization of the signature'''
        # convert r to bytes
        rb = self.r.to_bytes(32, 'big')
        # if r negative, add a 0x00
        if rb[0] >= 0x80:
            rb = b'\x00' + rb
        result = bytes([2, len(rb)]) + rb
        # convert s to bytes
        sb = self.s.to_bytes(32, 'big')
        # if s negative, add a 0x00
        if sb[0] >= 0x80:
            sb = b'\x00' + sb
        result += bytes([2, len(sb)]) + sb
        return bytes([0x30, len(result)]) + result

    @classmethod
    def parse(cls, signature_bin):
        s = BytesIO(signature_bin)
        compound = s.read(1)[0]
        if compound != 0x30:
            raise SyntaxError("Bad Signature")
        length = s.read(1)[0]
        if length + 2 != len(signature_bin):
            raise SyntaxError("Bad Signature Length")
        marker = s.read(1)[0]
        if marker != 0x02:
            raise SyntaxError("Bad Signature")
        rlength = s.read(1)[0]
        r = int.from_bytes(s.read(rlength), 'big')
        marker = s.read(1)[0]
        if marker != 0x02:
            raise SyntaxError("Bad Signature")
        slength = s.read(1)[0]
        s = int.from_bytes(s.read(slength), 'big')
        if len(signature_bin) != 6 + rlength + slength:
            raise SyntaxError("Signature too long")
        return cls(r, s)


    def __repr__(self):
        return 'Signature({:x}, {:x})'.format(self.r, self.s)
