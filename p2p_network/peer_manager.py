import json, os, time

class PeerManager:
    def __init__(self, peers_file="peers.json"):
        self.peers_file = peers_file
        self.peers = {}
        self.load_peers()

    def load_peers(self):
        if os.path.exists(self.peers_file):
            with open(self.peers_file) as f:
                self.peers = json.load(f)

    def save_peers(self):
        with open(self.peers_file, "w") as f:
            json.dump(self.peers, f, indent=2)

    def add_peer(self, peer_id, ip, port):
        self.peers[peer_id] = {"ip": ip, "port": port, "last_seen": time.time()}
        self.save_peers()

    def list_peers(self):
        return self.peers
