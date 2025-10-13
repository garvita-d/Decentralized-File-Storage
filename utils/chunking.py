# utils/chunker.py
import hashlib
import os

def chunk_file(file_path, chunk_size=1024*1024):
    """Splits file into chunks, saves as chunks/<hash>.chunk and returns list of hashes."""
    os.makedirs('chunks', exist_ok=True)
    chunks = []
    with open(file_path, 'rb') as f:
        index = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h = hashlib.sha256(chunk).hexdigest()
            filename = os.path.join('chunks', f'{h}.chunk')
            with open(filename, 'wb') as cf:
                cf.write(chunk)
            chunks.append(h)
            index += 1
    return chunks

def make_manifest(filename, chunk_hashes):
    """Create a small manifest mapping filename -> ordered chunk hashes"""
    return {'filename': filename, 'chunks': chunk_hashes}
    
import json

def save_manifest(manifest, output_dir='manifests'):
    """Save manifest JSON file to manifests/<filename>.manifest.json"""
    os.makedirs(output_dir, exist_ok=True)
    filename = manifest['filename']
    outpath = os.path.join(output_dir, f"{filename}.manifest.json")
    with open(outpath, 'w') as f:
        json.dump(manifest, f, indent=2)
    return outpath
