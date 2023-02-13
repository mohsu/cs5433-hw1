import hashlib
import itertools
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
from tqdm import tqdm

k = 4
n = 28
N = 16 ** 8


def get_watermark_hex(netid: str):
    watermark = bin(int(hashlib.sha256(netid.encode()).hexdigest(), base=16)).lstrip(
        '0b').zfill(16)[:16]
    watermark_hex = hex(int(watermark, 2)).lstrip('0x')
    return watermark, watermark_hex


def hash_hex_value(c_i):
    c_i_hash = bin(int(hashlib.sha256(bytes.fromhex(
        c_i)).hexdigest(), base=16)).lstrip('0b').zfill(256)[:n]
    return c_i_hash


def generate_coin(watermark_hex, i):
    hex = watermark_hex + format(i, '06x')
    hashed_hex = hash_hex_value(hex)
    return hex, hashed_hex


chuck = 100000


def generate_k_coins(watermark_hex, k):
    hashes = defaultdict(set)
    with tqdm(total=N) as pbar:
        with ThreadPoolExecutor(max_workers=10) as executor:
            for i in range(chuck):
                start, end = N // chuck * i, N // chuck * (i + 1)
                futures = {executor.submit(
                    generate_coin, watermark_hex, i): i for i in range(start, end)}

                for future in as_completed(futures):
                    h, hashed_h = future.result()
                    # print(h, hashed_h)
                    pbar.update(1)
                    hashes[hashed_h].add(h)

                    if len(hashes[hashed_h]) >= k:
                        return hashes[hashed_h]

    return None


def forge_nid(watermark_hex):
    l_comb = []
    for i in range(2, 4):
        l_comb += itertools.combinations(string.ascii_lowercase, i)
    d_comb = []
    for d in range(1, 11):
        d_comb += itertools.combinations(string.digits, d)

    for l in l_comb:
        for d in d_comb:
            f_netid = "".join(l + d)
            _, f_watermark_hex = get_watermark_hex(f_netid)
            if f_watermark_hex == watermark_hex:
                return f_netid


if __name__ == "__main__":
    netid = "yh863"
    watermark, watermark_hex = get_watermark_hex(
        netid)  # 1011110111111100, bdfc

    # C = generate_k_coins(watermark_hex, k)
    # print(C)  # ['bdfc1a2a6b', 'bdfc0a8735', 'bdfc25d389', 'bdfc07eb76']

    f_nid = forge_nid(watermark_hex)
    print(f_nid)  # ai34569
