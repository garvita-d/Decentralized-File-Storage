import os, json, asyncio, httpx, argparse
from src.common.hashing import sha256_hex

def chunk_bytes(data: bytes, size: int):
    for i in range(0, len(data), size):
        yield data[i:i+size]

async def register_chunk(dht_host: str, dht_port: int, chunk_hash: str, peers):
    url = f"http://{dht_host}:{dht_port}/store"
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.post(url, json={"key": chunk_hash, "value": {"peers": peers}})
        r.raise_for_status()

def save_chunk(storage_dir: str, chunk_hash: str, data: bytes):
    os.makedirs(storage_dir, exist_ok=True)
    with open(os.path.join(storage_dir, chunk_hash), "wb") as f:
        f.write(data)

async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="Path to input file to split")
    ap.add_argument("--chunk_size", type=int, default=1024*1024)
    ap.add_argument("--dht_host", default="127.0.0.1")
    ap.add_argument("--dht_port", type=int, default=7001)
    ap.add_argument("--peer_ports", type=str, default="7002,7003", help="ports that will host chunks")
    args = ap.parse_args()

    data = open(args.file, "rb").read()
    chunks = list(chunk_bytes(data, args.chunk_size))
    hashes = [sha256_hex(c) for c in chunks]

    peer_ports = [int(p.strip()) for p in args.peer_ports.split(",") if p.strip()]

    for i, (h, c) in enumerate(zip(hashes, chunks)):
        assigned_port = peer_ports[i % len(peer_ports)]
        storage_dir = f"./storage/{assigned_port}"
        save_chunk(storage_dir, h, c)
        await register_chunk(args.dht_host, args.dht_port, h, [{"host":"127.0.0.1","port":assigned_port}])

    manifest = {
        "fileId": os.path.basename(args.file) + ".reconstructed",
        "totalChunks": len(chunks),
        "chunkHashes": hashes,
        "chunkSize": args.chunk_size
    }
    with open("manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Created manifest.json with {len(chunks)} chunks.")

if __name__ == "__main__":
    asyncio.run(main())
