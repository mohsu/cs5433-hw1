from signature import MTSignature
import string
import random

S2 = MTSignature(10, 2)
S2.KeyGen(2023)
msg = "hello"
signature = S2.Sign(msg)

while True:
    length = random.randint(1, 100)
    forgery = "".join(random.choices(string.ascii_letters, k=length))
    if S2.Sign(forgery) == signature:
        print(forgery)
        break
