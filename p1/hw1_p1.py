import hashlib
import random
import string

k = 4
n = 28


def generate_hex_value(prefix):
    characters = string.hexdigits[:16]
    value = prefix + "".join(random.choice(characters) for _ in range(12))
    return value


def hash_hex_value(c_i):
    c_i_hash = bin(int(hashlib.sha256(bytes.fromhex(
        c_i)).hexdigest(), base=16)).lstrip('0b').zfill(256)[:n]
    return c_i_hash


def generate_k_coins(watermark_hex, k):
    d = generate_hex_value(watermark_hex)
    hashed_d = hash_hex_value(d)
    C = [d]
    while len(C) < k:
        hex = generate_hex_value(watermark_hex)
        hashed_hex = hash_hex_value(hex)
        if hashed_hex == hashed_d:
            C.append(hex)
            print(hex)
    return C


if __name__ == "__main__":
    netid = "yh863"
    watermark = bin(int(hashlib.sha256(netid.encode()).hexdigest(), base=16)).lstrip(
        '0b').zfill(16)[:16]  # watermark = 1011110111111100
    watermark_hex = hex(int(watermark, 2)).lstrip('0x')  # watermark_hex = bdfc

    C = generate_k_coins(watermark_hex, k)
    print(C)
