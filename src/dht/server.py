import os
import time
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

from .routing import RoutingTable, Contact
from .id import random_node_id
from ..common.hashing import sha256_hex


class StoreBody(BaseModel):
    key: str
    value: Any


class FindNodeBody(BaseModel):
    target: str


class FindValueBody(BaseModel):
    key: str


class DHTNode:
    def __init__(self, host: str, port: int, bootstrap: List[Dict[str, Any]]):
        self.host = host
        self.port = port
        self.node_id = random_node_id()
        self.id_hex = self.node_id.hex()
        self.rt = RoutingTable(self.node_id)
        self.store: Dict[str, Any] = {}
        self.storage_dir = os.environ.get("STORAGE_DIR", f"./storage/{self.port}")
        os.makedirs(self.storage_dir, exist_ok=True)

        self.rt.add(Contact(id_hex=self.id_hex, host=self.host, port=self.port, last_seen=time.time()))
        for peer in bootstrap:
            if peer.get("host") == self.host and peer.get("port") == self.port:
                continue
            pid = peer.get("id") or self.id_hex
            self.rt.add(Contact(id_hex=pid, host=peer["host"], port=peer["port"], last_seen=time.time()))

    def app(self) -> FastAPI:
        app = FastAPI()

        @app.post("/ping")
        def ping():
            return {"ok": True, "id": self.id_hex}

        @app.post("/store")
        def store(body: StoreBody):
            if not body.key:
                raise HTTPException(400, "missing key")
            self.store[body.key] = body.value
            return {"ok": True}

        @app.post("/find_node")
        def find_node(body: FindNodeBody):
            contacts = [
                {"id": c.id_hex, "host": c.host, "port": c.port}
                for c in self.rt.closest(body.target, 20)
            ]
            return {"ok": True, "contacts": contacts}

        @app.post("/find_value")
        def find_value(body: FindValueBody):
            if body.key in self.store:
                return {"ok": True, "value": self.store[body.key]}
            contacts = [
                {"id": c.id_hex, "host": c.host, "port": c.port}
                for c in self.rt.closest(body.key, 20)
            ]
            return {"ok": True, "contacts": contacts}

        @app.get("/chunks/{chunk_hash}")
        def get_chunk(chunk_hash: str):
            try:
                bytes.fromhex(chunk_hash)
            except Exception:
                raise HTTPException(400, "invalid chunk hash")
            p = os.path.join(self.storage_dir, chunk_hash)
            if not os.path.exists(p):
                raise HTTPException(404, "chunk not found")
            with open(p, "rb") as f:
                data = f.read()
            if sha256_hex(data) != chunk_hash:
                raise HTTPException(500, "stored chunk corrupted")
            return Response(content=data, media_type="application/octet-stream")

        return app


# ✅ Simple wrapper for orchestrator imports
class DHTServer:
    """Wrapper to run a simple DHT HTTP server compatible with orchestrator."""

    def __init__(self, host="127.0.0.1", port=8000):
        self.host = host
        self.port = port
        self.app = FastAPI()

        # In-memory store: chunk_hash -> node_addr
        self.DHT_STORAGE: Dict[str, str] = {}

        @self.app.post("/register")
        def register_chunk(req: Dict[str, Any]):
            chunk_hash = req.get("chunk_hash")
            node_addr = req.get("node_addr")
            if not chunk_hash or not node_addr:
                raise HTTPException(400, "Missing fields")
            self.DHT_STORAGE[chunk_hash] = node_addr
            print(f"[DHTServer] Registered {chunk_hash[:8]}... → {node_addr}")
            return {"status": "ok"}

        @self.app.get("/lookup/{chunk_hash}")
        def lookup_chunk(chunk_hash: str):
            node_addr = self.DHT_STORAGE.get(chunk_hash)
            if not node_addr:
                raise HTTPException(404, "Chunk not found")
            print(f"[DHTServer] Found {chunk_hash[:8]}... at {node_addr}")
            return {"node_addr": node_addr}
# ✅ Define a global FastAPI app for uvicorn
server = DHTServer()
server_app = server.app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.dht.server:server_app", host="127.0.0.1", port=8000, reload=True)

