"""
API Server for Decentralized File Storage Frontend
This bridges the web UI with your existing backend
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import os
import json
import asyncio
import httpx
from typing import List, Dict
from src.common.hashing import sha256_hex
from src.dht.routing import Contact
from src.retrieval.manifest import Manifest
from src.retrieval.retriever import retrieve_file

app = FastAPI(title="Decentralized Storage API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
DHT_HOST = "127.0.0.1"
DHT_PORT = 7001
STORAGE_NODES = [7002, 7003]
CHUNK_SIZE = 1024 * 1024  # 1MB
MANIFESTS_DIR = "manifests"
DOWNLOADS_DIR = "downloads"

os.makedirs(MANIFESTS_DIR, exist_ok=True)
os.makedirs(DOWNLOADS_DIR, exist_ok=True)


def chunk_bytes(data: bytes, size: int):
    """Split data into chunks"""
    for i in range(0, len(data), size):
        yield data[i:i+size]


async def register_chunk(chunk_hash: str, peers: List[Dict]):
    """Register chunk in DHT"""
    url = f"http://{DHT_HOST}:{DHT_PORT}/store"
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.post(url, json={"key": chunk_hash, "value": {"peers": peers}})
        r.raise_for_status()


def save_chunk(storage_dir: str, chunk_hash: str, data: bytes):
    """Save chunk to storage directory"""
    os.makedirs(storage_dir, exist_ok=True)
    with open(os.path.join(storage_dir, chunk_hash), "wb") as f:
        f.write(data)


@app.get("/")
async def root():
    return {
        "message": "Decentralized File Storage API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/api/upload",
            "download": "/api/download/{file_id}",
            "files": "/api/files",
            "search": "/api/search/{hash}",
            "nodes": "/api/nodes"
        }
    }


@app.get("/api/nodes")
async def get_nodes_status():
    """Check status of all nodes"""
    nodes = [
        {"name": "DHT Node", "host": DHT_HOST, "port": DHT_PORT},
        {"name": "Storage Node 1", "host": DHT_HOST, "port": 7002},
        {"name": "Storage Node 2", "host": DHT_HOST, "port": 7003},
    ]
    
    results = []
    for node in nodes:
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.post(f"http://{node['host']}:{node['port']}/ping")
                results.append({
                    **node,
                    "status": "online" if response.status_code == 200 else "offline"
                })
        except:
            results.append({**node, "status": "offline"})
    
    return {"nodes": results}


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file to the decentralized network"""
    try:
        # Read file data
        data = await file.read()
        
        # Split into chunks
        chunks = list(chunk_bytes(data, CHUNK_SIZE))
        chunk_hashes = [sha256_hex(c) for c in chunks]
        
        # Distribute chunks across storage nodes
        for i, (chunk_hash, chunk_data) in enumerate(zip(chunk_hashes, chunks)):
            assigned_port = STORAGE_NODES[i % len(STORAGE_NODES)]
            storage_dir = f"./storage/{assigned_port}"
            
            # Save chunk locally
            save_chunk(storage_dir, chunk_hash, chunk_data)
            
            # Register in DHT
            await register_chunk(
                chunk_hash, 
                [{"host": DHT_HOST, "port": assigned_port}]
            )
        
        # Create manifest
        manifest = {
            "fileId": file.filename,
            "originalName": file.filename,
            "totalChunks": len(chunks),
            "chunkHashes": chunk_hashes,
            "chunkSize": CHUNK_SIZE,
            "size": len(data)
        }
        
        # Save manifest
        manifest_path = os.path.join(MANIFESTS_DIR, f"{file.filename}.json")
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
        
        return {
            "status": "success",
            "message": f"File uploaded successfully",
            "fileId": file.filename,
            "chunks": len(chunks),
            "hash": chunk_hashes[0],
            "manifest": manifest
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/files")
async def list_files():
    """List all uploaded files"""
    try:
        files = []
        if os.path.exists(MANIFESTS_DIR):
            for filename in os.listdir(MANIFESTS_DIR):
                if filename.endswith('.json'):
                    try:
                        with open(os.path.join(MANIFESTS_DIR, filename)) as f:
                            manifest = json.load(f)
                            files.append({
                                "name": manifest.get("originalName", manifest.get("fileId", filename.replace(".json", ""))),
                                "hash": manifest["chunkHashes"][0] if manifest.get("chunkHashes") else "unknown",
                                "chunks": manifest.get("totalChunks", 0),
                                "size": manifest.get("size", 0)
                            })
                    except Exception as e:
                        print(f"Error reading manifest {filename}: {e}")
                        continue
        
        # Sort by most recent first (assuming filename contains timestamp or reverse list)
        files.reverse()
        
        return {"files": files}
    except Exception as e:
        print(f"Error listing files: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/search/{hash}")
async def search_by_hash(hash: str):
    """Search for a file by its content hash"""
    try:
        # Search in manifests
        if os.path.exists(MANIFESTS_DIR):
            for filename in os.listdir(MANIFESTS_DIR):
                if filename.endswith('.json'):
                    with open(os.path.join(MANIFESTS_DIR, filename)) as f:
                        manifest = json.load(f)
                        if hash in manifest["chunkHashes"]:
                            return {
                                "found": True,
                                "file": {
                                    "name": manifest.get("originalName", filename),
                                    "hash": hash,
                                    "chunks": manifest["totalChunks"],
                                    "size": manifest.get("size", 0)
                                }
                            }
        
        return {"found": False, "message": "File not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/{file_id}")
async def download_file_endpoint(file_id: str):
    """Download a file by reconstructing it from chunks"""
    try:
        # Find manifest
        manifest_path = os.path.join(MANIFESTS_DIR, f"{file_id}.json")
        
        if not os.path.exists(manifest_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Load manifest
        with open(manifest_path) as f:
            manifest_data = json.load(f)
        
        manifest = Manifest(**manifest_data)
        
        # Create bootstrap contacts
        bootstrap = [Contact(
            id_hex="0"*40, 
            host=DHT_HOST, 
            port=DHT_PORT
        )]
        
        # Retrieve file
        output_path = await retrieve_file(manifest, bootstrap, out_dir=DOWNLOADS_DIR)
        
        return FileResponse(
            output_path,
            media_type="application/octet-stream",
            filename=file_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Decentralized Storage API Server...")
    print("📡 API will be available at: http://127.0.0.1:8080")
    print("📝 API Documentation: http://127.0.0.1:8080/docs")
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")