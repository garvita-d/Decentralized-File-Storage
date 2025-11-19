# tests/test_chunking.py
import os
import hashlib
from utils.chunking import chunk_file, make_manifest

def test_small_file_chunking(tmp_path):
    # Create small file (<1 MB)
    file_path = tmp_path / "small.txt"
    file_path.write_text("hello world")

    chunks = chunk_file(file_path, chunk_size=1024*1024)
    assert len(chunks) == 1, "Small file should create only one chunk"

    # Verify chunk file exists
    chunk_filename = os.path.join("chunks", f"{chunks[0]}.chunk")
    assert os.path.exists(chunk_filename), "Chunk file missing"

def test_large_file_chunking(tmp_path):
    # Create large file (>10 MB)
    file_path = tmp_path / "large.bin"
    with open(file_path, "wb") as f:
        f.write(os.urandom(11 * 1024 * 1024))  # 11 MB

    chunks = chunk_file(file_path, chunk_size=1024*1024)
    assert len(chunks) >= 10, "Expected multiple chunks for large file"

def test_hash_consistency(tmp_path):
    # Create same content twice
    f1 = tmp_path / "a.txt"
    f2 = tmp_path / "b.txt"
    f1.write_text("consistent data")
    f2.write_text("consistent data")

    chunks1 = chunk_file(f1)
    chunks2 = chunk_file(f2)
    assert chunks1 == chunks2, "Same file should produce same hashes"

def test_manifest_creation(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("abc")
    chunks = chunk_file(file_path)
    manifest = make_manifest(str(file_path), chunks)
    assert manifest["filename"].endswith("test.txt")
    assert manifest["chunks"] == chunks

