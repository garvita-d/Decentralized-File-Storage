import json, argparse, asyncio
from src.retrieval.manifest import Manifest
from src.retrieval.retriever import retrieve_file
from src.dht.routing import Contact

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="manifest.json")
    ap.add_argument("--bootstrap", default='[{"host":"127.0.0.1","port":7001}]',
                    help='JSON list of contacts e.g. [{"host":"127.0.0.1","port":7001}]')
    args = ap.parse_args()

    manifest = Manifest(**json.load(open(args.manifest)))
    bs_cfg = json.loads(args.bootstrap)
    bootstrap = [Contact(id_hex="0"*40, host=c["host"], port=c["port"]) for c in bs_cfg]

    out_path = asyncio.run(retrieve_file(manifest, bootstrap))
    print(f"Saved file to: {out_path}")

if __name__ == "__main__":
    main()
