import argparse
import uvicorn
import json
from src.dht.server import DHTNode

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=7001)
    ap.add_argument("--bootstrap", default='[]', help="JSON list of peers [{host,port,id?}]")
    ap.add_argument("--storage_dir", default=None, help="Directory to store chunks (overrides default)")
    args = ap.parse_args()

    bootstrap = json.loads(args.bootstrap)
    node = DHTNode(args.host, args.port, bootstrap)
    if args.storage_dir:
        import os
        node.storage_dir = args.storage_dir
        os.makedirs(node.storage_dir, exist_ok=True)

    app = node.app()
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")

if __name__ == "__main__":
    main()
