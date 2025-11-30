import argparse
import json
import os

import uvicorn
from src.dht.server import DHTNode


def parse_bootstrap(raw: str):
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("\n❌ Invalid --bootstrap format.")
        print("   It must be valid JSON.")
        print("   Example:")
        print('   --bootstrap \'[{"host": "127.0.0.1", "port": 7001}]\'\n')
        raise SystemExit(1)

    if not isinstance(data, list):
        print("\n❌ --bootstrap must be a JSON list.")
        print("   Example:")
        print('   --bootstrap \'[{"host": "127.0.0.1", "port": 7001}]\'\n')
        raise SystemExit(1)

    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a DHT node using uvicorn.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7001)
    parser.add_argument(
        "--bootstrap",
        default="[]",
        help='JSON list of peers, e.g. \'[{"host":"127.0.0.1","port":7001}]\'',
    )
    parser.add_argument(
        "--storage_dir",
        default=None,
        help="Directory to store chunks (overrides default).",
    )

    args = parser.parse_args()

    bootstrap = parse_bootstrap(args.bootstrap)

    node = DHTNode(args.host, args.port, bootstrap)

    if args.storage_dir:
        node.storage_dir = args.storage_dir
        os.makedirs(node.storage_dir, exist_ok=True)

    app = node.app()
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
