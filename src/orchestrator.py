# src/orchestrator.py
import os
from src.utils.chunking import chunk_file, make_manifest, save_manifest
from src.dht.client import DHTClient
from src.node.network import send_chunk, retrieve_chunk

dht_client = DHTClient("http://127.0.0.1:8000")

def upload_file(file_path, node_address):
    chunks = chunk_file(file_path)
    manifest = make_manifest(os.path.basename(file_path), chunks)
    save_manifest(manifest)
    for ch in chunks:
        chunk_path = os.path.join('chunks', f'{ch}.chunk')
        send_chunk(chunk_path, node_address)
        dht_client.register_chunk(ch, node_address)
    return manifest

def download_file(manifest, output_path):
    with open(output_path, 'wb') as out_f:
        for ch in manifest['chunks']:
            node_addr = dht_client.lookup_chunk(ch)
            if not node_addr:
                raise Exception(f"No node for chunk {ch}")
            data = retrieve_chunk(ch, node_addr)
            out_f.write(data)