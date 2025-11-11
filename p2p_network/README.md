---


# 🌐 P2P Network Module

## 📘 Overview
The **Peer-to-Peer (P2P) Network** module forms the communication layer of the *Decentralized File Storage* system.  
It enables peers to directly connect, share, and retrieve file chunks without relying on a central server.  
Each node (peer) acts as both a **client** and a **server**, maintaining a resilient and distributed file-sharing network.

---

## ⚙️ Key Features
- 🔗 **Peer Discovery:** Nodes can dynamically connect and exchange peer lists.
- 📡 **Message Exchange:** Custom message protocol for request, response, and acknowledgment.
- 📁 **File Chunk Transfer:** Supports sending and receiving file parts.
- 🧠 **Peer Management:** Keeps track of connected peers, handles join and leave events.
- 🧰 **Modular Architecture:** Works alongside Chunking, DHT, and File Retrieval modules.
- 🔒 **Extensible:** Can later include encryption and checksum verification.

---

## 🗂 Folder Structure
```

p2p_network/
│
├── peer.py                → Initializes a peer node, listens for connections
├── client.py              → Connects to other peers and sends requests
├── peer_manager.py        → Maintains list of active peers and manages connections
├── file_transfer.py       → Handles chunk upload/download between peers
├── message_protocol.py    → Defines message formats (REQ, RES, ACK, FILE, JOIN)
├── network_manager.py     → Coordinates overall peer communication and routing
├── utils.py               → Helper functions (socket setup, logging, config)
└── README.md              → Documentation for this module

````

---

## 🚀 How to Run the Module

### 1️⃣ Start a Peer Node
Run this command to start a peer server:
```bash
python peer.py
````

Output example:

```
[STARTED] Peer active on 127.0.0.1:5000
[WAITING] Listening for incoming peer connections...
```

---

### 2️⃣ Connect Another Peer

Open another terminal and run:

```bash
python client.py
```

This will connect the second peer to the first node.

You’ll see logs like:

```
[CONNECTED] Connected to peer 127.0.0.1:5000
[SENT] Message: REQ File_Chunk_1
[RECEIVED] Acknowledgment from peer
```

---

### 3️⃣ Send or Receive a File Chunk

To simulate a file transfer:

```bash
python file_transfer.py
```

This handles sending or receiving chunks between connected peers using sockets.

---

### 4️⃣ Manage Peers

`peer_manager.py` keeps track of:

* Active peers (via IP and port)
* Connection timeouts
* Peer addition/removal on disconnect

Run for debugging:

```bash
python peer_manager.py
```

---

### 5️⃣ Stop the Peer Node

To stop a running peer safely:

* Press **Ctrl + C**, or
* Type `"exit"` (if supported in your peer’s command loop).

---

## 🧠 Integration with Other Modules

This module interacts with the following parts of the system:

* **Chunking & Hashing:** to verify chunk integrity before transfer
* **DHT Module:** to locate peers storing specific chunks
* **File Retrieval:** to assemble the complete file from received parts

All modules together form a **fully decentralized and fault-tolerant file sharing system**.

---

## 🔮 Future Enhancements

* Peer discovery using tracker or gossip protocol
* End-to-end encryption for secure file transfer
* Improved fault tolerance with retry mechanisms
* Asynchronous networking for better scalability
* Integration with GUI frontend for peer visualization

---

## 🧑‍💻 Contributor

**Module:** P2P Network
**Member:** Anya Kalluri
**Branch:** `p2p-network`

---

## 🏁 Summary

The **P2P Network module** is the backbone of the decentralized system, enabling:

* Direct peer connections
* Reliable and scalable data exchange
* Secure and extensible file-sharing functionality

It ensures the system remains **fully decentralized**, resilient, and efficient — without any single point of failure.



---

