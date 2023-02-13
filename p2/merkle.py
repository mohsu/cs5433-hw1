from typing import Optional, List
from hashlib import sha256


def H(obj: str) -> str:
    h = sha256(obj.encode()).hexdigest()
    return h


def verify(obj: str, proof: str, commitment: str) -> bool:
    h = H(obj)

    if proof:
        for s in proof.split(";"):
            index, sib_h = s.split(",")
            if not sib_h:
                continue
            if int(index) % 2 == 0:
                h = H(h + sib_h)
            else:
                h = H(sib_h + h)
    return h == commitment


class Prover:
    def __init__(self):
        self.objects = []
        self.tree = []
        self.root = None

    # Build a merkle tree and return the commitment
    def build_merkle_tree(self, objects: List[str]) -> str:
        self.objects = objects
        nodes = [H(obj) for obj in objects]
        self.tree.append(nodes)

        while len(nodes) > 1:
            upper_nodes = []
            for i in range(0, len(nodes), 2):
                node1 = nodes[i]
                if i + 1 < len(nodes):
                    node2 = nodes[i + 1]
                    new_node = H(node1 + node2)
                else:
                    new_node = node1
                upper_nodes.append(new_node)

            self.tree.append(upper_nodes)
            nodes = upper_nodes

        self.root = nodes[0]
        return self.root

    def get_leaf(self, index: int) -> Optional[str]:
        if index < 0 or index >= len(self.objects):
            return None

        return self.objects[index]

    def generate_proof(self, index: int) -> Optional[str]:
        if index < 0 or index >= len(self.objects):
            return None

        proof = []
        layer = 0
        while layer < len(self.tree) - 1:
            if index % 2 == 0:
                if index + 1 < len(self.tree[layer]):
                    proof.append(f"{index},{self.tree[layer][index + 1]}")
                else:
                    proof.append(f"{index},")
            else:
                proof.append(f"{index},{self.tree[layer][index - 1]}")
            layer += 1
            index = index // 2

        return ";".join(proof)


"""
[Example 1]
     0
   0   1
 0   1   2
0 1 2 3 4 5

index = 3, layer = 0
proof = [2]

index = 3 // 2 = 1, layer = 1
proof = [2, 1]

index = 1 // 2 = 0, layer = 2
proof = [2, 1, 0]

# Verfify
h = H(3)

i = 0
h = H(proof[0] + h)

i = 1
h = H(proof[1] + h)

i = 2
h = H(h + proof[2])

commitment == h


[Example 2]
  0
 0 1
0 1 2

proof = [1]

"""
