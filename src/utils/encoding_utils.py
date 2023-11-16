import hashlib


def hash256(s):
    # Double SHA-256 Hashing
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


def hash160(s):
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()


def encode_base58_checksum(b):
    return encode_base58(b + hash256(b)[:4])


def encode_base58(s):
    base58_alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    value = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while value > 0:
        value, mod = divmod(value, 58)
        result = base58_alphabet[mod] + result
    return prefix + result


def decode_base58(s):
    base58_alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    result = 0
    for c in s:
        result *= 58
        result += base58_alphabet.index(c)
    # Calculate the number of bytes needed
    byte_length = (result.bit_length() + 7) // 8
    return result.to_bytes(byte_length, 'big')