from hashlib import sha256

def sha256_hex(b: bytes) -> str:
    return sha256(b).hexdigest()
