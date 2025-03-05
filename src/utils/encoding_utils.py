import hashlib
from Crypto.Hash import RIPEMD160


def ripemd160_hash(data: bytes) -> str:
    """Compute the RIPEMD-160 hash of the input data securely."""
    h = RIPEMD160.new()
    h.update(data)
    return h.hexdigest()

# Example usage
data = b"Secure RIPEMD-160 in Python"
hashed_value = ripemd160_hash(data)
print("RIPEMD-160 Hash:", hashed_value)


def hash256(s):
    # Double SHA-256 Hashing
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


def hash160(s):
    hash_str = ripemd160_hash(hashlib.sha256(s).digest())
    hash_bytes = bytes.fromhex(hash_str)
    return hash_bytes


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


def little_endian_to_int(le_bytes):
    return int.from_bytes(le_bytes, 'little')


def int_to_little_endian(val, length):
    return val.to_bytes(length, 'little')
