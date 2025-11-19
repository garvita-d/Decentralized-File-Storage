# src/node/network.py
import requests
import os

def send_chunk(chunk_path, node_addr):
    chunk_hash = os.path.basename(chunk_path).replace(".chunk", "")
    with open(chunk_path, 'rb') as f:
        # IMPORTANT: filename MUST be the chunk hash
        files = {'file': (chunk_hash, f)}
        r = requests.post(f"{node_addr}/upload", files=files)

    if r.status_code != 200:
        raise Exception(f"Upload failed: {r.text}")
    return r.status_code
    
def retrieve_chunk(chunk_hash, node_addr):
    r = requests.get(f"{node_addr}/download/{chunk_hash}")
    if r.status_code != 200:
        raise Exception(f"Download failed: {r.text}")
    return r.content
