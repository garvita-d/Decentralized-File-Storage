import httpx
from typing import Any, Dict
# src/dht/client.py
import requests

class DHTClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    def register_chunk(self, chunk_hash, node_addr):
        r = requests.post(f"{self.base_url}/register", json={"chunk_hash": chunk_hash, "node_addr": node_addr})
        return r.status_code

    def lookup_chunk(self, chunk_hash):
        r = requests.get(f"{self.base_url}/lookup/{chunk_hash}")
        if r.status_code == 200:
            return r.json().get("node_addr")
        return None


async def rpc(host: str, port: int, path: str, body: Dict[str, Any], timeout=3.0) -> Dict[str, Any]:
    url = f"http://{host}:{port}{path}"
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(url, json=body)
        r.raise_for_status()
        return r.json()
