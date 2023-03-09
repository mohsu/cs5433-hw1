""" Script to verify that a coin is properly formatted, according to the specification of homework 1's writeup.

To run, supply your coin.txt file and your watermark (as a bit string) as the first and second command line parameters, respectively.

Example: python3 hw1_p1_verify_coin.py coin.txt 100001100111
"""


import sys
import hashlib


k = 4
n = 28
watermark_length = 4


def verify_coin(coin_txt, watermark_hex):
    if len(watermark_hex) != watermark_length:
        return False
    d = None
    with open(coin_txt) as f:
        for i, c_i in enumerate(f):
            c_i_hash = bin(int(hashlib.sha256(bytes.fromhex(
                c_i)).hexdigest(), base=16)).lstrip('0b').zfill(256)[:n]
            print(c_i_hash)
            if i == 0:
                d = c_i_hash
            if c_i[:watermark_length] != watermark_hex or c_i_hash != d:
                return False

    return False if i+1 != k else True


if __name__ == "__main__":
    coin_txt, watermark = sys.argv[1:]
    l = (len(watermark) + 3) // 4
    watermark_hex = '{:0{}x}'.format(int(watermark, 2), l)
    # watermark_hex = hex(int(watermark, 2)).lstrip('0x')
    print(watermark_hex)
    if verify_coin(coin_txt, watermark_hex):
        print("Your coin is valid!")
    else:
        print("Your coin is not valid!")
    
    forged_netid = "fl012679"
    w_forged = bin(int(hashlib.sha256(forged_netid.encode()).hexdigest(), base=16)).lstrip('0b').zfill(256)[:16]
    l = (len(w_forged) + 3) // 4
    f_watermark_hex = '{:0{}x}'.format(int(w_forged, 2), l)
    # f_watermark_hex = hex(int(w_forged, 2)).lstrip('0x')
    print(f"Forged netid has watermark: {w_forged}, and is the same hex and original one:", f_watermark_hex == watermark_hex)

"""
Example:

netid = "af535"
watermark = bin(int(hashlib.sha256(netid.encode()).hexdigest(), base=16)).lstrip('0b').zfill(16)[:16]  # w = 1000011001111010
watermark_hex = hex(int(watermark, 2)).lstrip('0x')  # 867a
C =(867a95c2a8781d95, 867a79c683c4b9de, 867a18839dcbd23f, 867aee195b47b3d2)

forged_netid = "qn00061"
w_forged = bin(int(hashlib.sha256(forged_netid.encode()).hexdigest(), base=16)).lstrip('0b').zfill(16)[:16]
f_watermark_hex = hex(int(w_forged, 2)).lstrip('0x')
print(f_watermark_hex == watermark_hex)
"""
