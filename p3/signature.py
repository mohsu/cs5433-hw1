import string
import random
import hashlib


def SHA(s: string) -> string:
    """return the hash of a string"""
    return hashlib.sha256(s.encode()).hexdigest()


def toDigit(s: string) -> int:
    """transfer a hex string to integer"""
    return int(s, 16)


def KeyPairGen(d: int, r: int) -> dict:
    """generate 2^d (si^{-1}, si) pairs based on seed r"""
    pairs = {}
    random.seed(r)
    for i in range(1 << d):
        cur = random.randbytes(32).hex()
        while cur in pairs:
            cur = random.randbytes(32).hex()
        pairs[cur] = SHA(cur)
    return pairs


class MTSignature:
    def __init__(self, d, k):
        self.d = d
        self.k = k
        self.treenodes = [None] * (d+1)
        for i in range(d+1):
            self.treenodes[i] = [None] * (1 << i)
        self.sk = [None] * (1 << d)
        self.pk = None  # same as self.treenodes[0][0]

    def KeyGen(self, seed: int) -> string:
        """Populate the fields self.treenodes, self.sk and self.pk.

        Args:
            seed (int): random seed

        Returns:
            string: self.pk
        """
        pairs = KeyPairGen(self.d, seed)

        for i, (s, p) in enumerate(pairs.items()):
            self.treenodes[self.d][i] = p
            self.sk[i] = s

        for layer in range(self.d - 1, -1, -1):
            nodes = self.treenodes[layer + 1]
            for j in range(len(nodes) // 2):
                node1, node2 = nodes[j * 2], nodes[j * 2 + 1]
                self.treenodes[layer][j] = SHA(
                    format(j, "b").zfill(256) + node1 + node2)

        self.pk = self.treenodes[0][0]
        return self.pk

    def Path(self, j: int) -> string:
        """The order in SPj follows from the leaf to the root.

        Args:
            j (int): index of the leaf node

        Returns:
            string: Returns the path SPj for the index j
        """
        path = ""
        for layer in range(self.d, 0, -1):
            if j % 2 == 0:
                path += f"{self.treenodes[layer][j + 1]}"
            else:
                path += f"{self.treenodes[layer][j - 1]}"
            j = j // 2
        return "".join(path)

    def Sign(self, msg: string) -> string:
        """The first is a sequence of sigma values and the second is a list of sibling paths.
        Each sibling path is in turn a d-length list of tree node values.
        All values are 64 bytes. Final signature is a single string obtained by concatentating all values.

        Args:
            msg (string): message to be signed

        Returns:
            string: Returns the signature. The format of the signature is as follows: ([sigma], [SP]).
        """
        sigmas = []
        signatures = []
        for j in range(1, self.k + 1):
            zj = toDigit(SHA(format(j, "b").zfill(256) + msg)) % (1 << self.d)
            sigmas.append(self.sk[zj])
            signatures.append(self.Path(zj))
        return "".join(sigmas) + "".join(signatures)
