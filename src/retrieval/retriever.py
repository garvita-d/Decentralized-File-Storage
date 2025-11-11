import asyncio
import httpx
import os
from typing import List, Dict, Any
from ..common.hashing import sha256_hex
from ..dht.kademlia import find_value
from ..dht.routing import Contact
from .manifest import Manifest

async def fetch_chunk_from_peer(peer: Dict[str, Any], chunk_hash: str, timeout=5.0) -> bytes:
    url = f"http://{peer['host']}:{peer['port']}/chunks/{chunk_hash}"
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.content

async def retrieve_file(manifest: Manifest, bootstrap: List[Contact], out_dir="downloads", concurrency=6) -> str:
    os.makedirs(out_dir, exist_ok=True)
    buffers: List[bytes] = [b""] * manifest.totalChunks

    sem = asyncio.Semaphore(concurrency)
    progress = 0

    async def worker(i: int):
        nonlocal progress
        chunk_hash = manifest.chunkHashes[i]
        async with sem:
            value = await find_value(bootstrap, chunk_hash)
            if not value or not isinstance(value, dict) or "peers" not in value or not value["peers"]:
                raise RuntimeError(f"No peers for chunk {i}")
            for p in value["peers"]:
                try:
                    data = await fetch_chunk_from_peer(p, chunk_hash)
                    if sha256_hex(data) != chunk_hash:
                        continue
                    buffers[i] = data
                    break
                except Exception:
                    continue
            else:
                raise RuntimeError(f"All peers failed for chunk {i}")
        progress += 1
        pct = int(progress * 100 / manifest.totalChunks)
        print(f"\rProgress: {pct}% ({progress}/{manifest.totalChunks})", end="", flush=True)

    await asyncio.gather(*(worker(i) for i in range(manifest.totalChunks)))
    print()

    out_path = os.path.join(out_dir, manifest.fileId)
    with open(out_path, "wb") as f:
        for b in buffers:
            f.write(b)
    return out_path
