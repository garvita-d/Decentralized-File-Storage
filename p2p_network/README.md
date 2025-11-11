---

## 🧩 P2P Network Module

### 📘 Overview

The **P2P (Peer-to-Peer) Network** module enables direct communication and data exchange between peers in the decentralized file storage system.
Each peer can act as both a **client** and a **server**, sharing file chunks without needing a centralized authority.

---

### ⚙️ Key Features

* Peer discovery and connection management
* Message exchange (request, response, acknowledgement)
* File chunk transfer between peers
* Lightweight socket-based communication
* Modular structure for integration with DHT and retrieval modules

---

### 🗂 Folder Structure

```
p2p_network/
│
├── peer.py               → Handles peer setup and server socket
├── client.py             → Connects to other peers and sends messages
├── message_protocol.py   → Defines message types and formats
├── network_manager.py    → Manages connected peers and routing
└── utils.py              → Helper functions for networking/logging
```

---

### 🚀 How to Run

#### **1. Start a Peer**

```bash
python peer.py
```

This will start a listening peer node on a given host and port.

#### **2. Connect Another Peer**

In another terminal:

```bash
python client.py
```

This connects to the first peer and sends a message or file request.

---

### 🧠 Future Improvements

* Peer discovery using gossip or tracker server
* File chunk verification using hashing
* Encrypted communication between peers
* NAT traversal and port forwarding support

---

### 🧑‍💻 Contributor

**Member 2:** *Anya Kalluri*
Module: **P2P Network**

---


