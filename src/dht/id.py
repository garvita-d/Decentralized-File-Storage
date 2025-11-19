import os
from hashlib import sha256

NODE_ID_BYTES = 20  # 160-bit

def node_id_from_string(s: str) -> bytes:
    full = sha256(s.encode("utf-8")).digest()  # 32 bytes
    return full[:NODE_ID_BYTES]

def random_node_id() -> bytes:
    return node_id_from_string(os.urandom(32).hex())

def xor_distance(a: bytes, b: bytes) -> int:
    return int.from_bytes(bytes(x ^ y for x, y in zip(a, b)), "big")
