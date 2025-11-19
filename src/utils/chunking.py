# src/utils/chunking.py
import os, hashlib, json

def chunk_file(file_path, chunk_size=1024*1024):
    os.makedirs('chunks', exist_ok=True)
    chunks = []
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h = hashlib.sha256(chunk).hexdigest()
            with open(os.path.join('chunks', f'{h}.chunk'), 'wb') as cf:
                cf.write(chunk)
            chunks.append(h)
    return chunks

def make_manifest(filename, chunk_hashes):
    return {'filename': filename, 'chunks': chunk_hashes}

def save_manifest(manifest, output_dir='manifests'):
    os.makedirs(output_dir, exist_ok=True)
    outpath = os.path.join(output_dir, f"{manifest['filename']}.manifest.json")
    with open(outpath, 'w') as f:
        json.dump(manifest, f, indent=2)
    return outpath
