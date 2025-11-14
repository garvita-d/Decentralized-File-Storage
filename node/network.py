# node/network.py
import requests

def send_chunk(chunk_path, node_addr):
    with open(chunk_path, 'rb') as f:
        r = requests.post(f"{node_addr}/upload", files={'file': f})
    print(f"[→] Sent chunk {chunk_path} → {node_addr} (status={r.status_code})")
    return r.status_code

def retrieve_chunk(chunk_hash, node_addr):
    r = requests.get(f"{node_addr}/download/{chunk_hash}")
    print(f"[←] Retrieved chunk {chunk_hash} from {node_addr} (size={len(r.content)} bytes)")
    return r.content
