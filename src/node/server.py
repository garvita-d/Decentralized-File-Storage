# src/node/server.py
import os, requests
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

DHT_URL = "http://127.0.0.1:8000"
app = FastAPI()
STORAGE_DIR = os.environ.get("STORAGE_DIR", "./storage/node1")
os.makedirs(STORAGE_DIR, exist_ok=True)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    data = await file.read()
    chunk_hash = file.filename  # orchestrator must use hash as filename when sending
    path = os.path.join(STORAGE_DIR, chunk_hash)
    with open(path, "wb") as f:
        f.write(data)
    # register to DHT
    node_addr = f"http://127.0.0.1:8001"
    try:
        requests.post(f"{DHT_URL}/register", json={"chunk_hash": chunk_hash, "node_addr": node_addr})
    except Exception as e:
        raise HTTPException(500, f"DHT registration failed: {e}")
    return {"status": "stored", "chunk_hash": chunk_hash}

@app.get("/download/{chunk_hash}")
def download_chunk(chunk_hash: str):
    path = os.path.join(STORAGE_DIR, chunk_hash)
    if not os.path.exists(path):
        raise HTTPException(404, "chunk not found")
    return FileResponse(path)

# run with: python src/node/server.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.node.server:app", host="127.0.0.1", port=8001, reload=True)
