# src/dht/dht.py
from src.dht.client import DHTClient
from src.dht.server import DHTServer

# For now, simulate DHT lookups in memory
dht_store = {}

def register_chunk(chunk_hash, node_address):
    """Register a chunk hash → node mapping"""
    dht_store[chunk_hash] = node_address
    print(f"[DHT] Registered {chunk_hash[:8]}... -> {node_address}")

def lookup_chunk(chunk_hash):
    """Lookup the node address that holds a chunk"""
    addr = dht_store.get(chunk_hash)
    print(f"[DHT] Lookup {chunk_hash[:8]}... -> {addr}")
    return addr
