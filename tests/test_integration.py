# tests/test_integration.py
from src.orchestrator import upload_file, download_file
import os

def test_end_to_end(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("hello decentralized storage" * 100)
    # ensure node and DHT are running on ports 8001 and 8000
    manifest = upload_file(str(f), "http://127.0.0.1:8001")
    out = tmp_path / "restored.txt"
    download_file(manifest, str(out))
    assert out.read_text() == f.read_text()
