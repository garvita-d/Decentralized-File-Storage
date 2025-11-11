from pydantic import BaseModel
from typing import List

class Manifest(BaseModel):
    fileId: str
    totalChunks: int
    chunkHashes: List[str]
    chunkSize: int
