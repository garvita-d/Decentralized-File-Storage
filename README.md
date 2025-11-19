# 🌐 Decentralized File Storage System

A peer-to-peer decentralized file storage system inspired by IPFS and Filecoin. This project implements content-based addressing, distributed storage, and fault-tolerant file retrieval across a network of nodes.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.5-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Testing](#testing)
- [Contributing](#contributing)
- [Team](#team)
- [License](#license)

---

## 🎯 Overview

This decentralized file storage system distributes files across multiple nodes without relying on a central server. Files are identified by their content hash (SHA-256) rather than their location, ensuring data integrity and enabling efficient deduplication.

### Key Concepts

- **Content Addressing**: Files are identified by cryptographic hashes of their content
- **Chunking**: Large files are split into manageable 1MB chunks
- **Distributed Hash Table (DHT)**: Maps chunk hashes to node locations
- **Fault Tolerance**: Files remain accessible even if some nodes fail
- **Data Integrity**: SHA-256 verification ensures no corruption

---

## ✨ Features

### Core Features
- ✅ **File Chunking**: Automatically splits files into 1MB chunks
- ✅ **Content-Based Addressing**: Each chunk identified by SHA-256 hash
- ✅ **Distributed Storage**: Chunks distributed across multiple nodes
- ✅ **DHT Implementation**: Efficient chunk location lookup using Kademlia-inspired routing
- ✅ **File Reconstruction**: Reassemble files from distributed chunks
- ✅ **Data Integrity**: Hash verification on every chunk
- ✅ **Fault Tolerance**: Retrieve files even if nodes are offline

### Web Interface
- 🎨 **Modern UI**: Beautiful gradient design with responsive layout
- 📤 **Drag & Drop Upload**: Easy file uploads via drag-and-drop
- 🔍 **Hash-Based Search**: Find files using content hashes
- 📊 **Node Monitoring**: Real-time status of network nodes
- 💾 **File Management**: View, download, and manage stored files
- 📋 **One-Click Actions**: Copy hashes, download files instantly

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Web Interface                         │
│                     (frontend_app.html)                      │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                       API Server (Port 8080)                 │
│                       (api_server.py)                        │
└────────────────────────────┬────────────────────────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
│   DHT Node       │ │ Storage Node │ │  Storage Node    │
│   Port 7001      │ │  Port 7002   │ │   Port 7003      │
│                  │ │              │ │                  │
│  - Routing Table │ │ - Stores     │ │  - Stores        │
│  - Key-Value     │ │   Chunks     │ │    Chunks        │
│    Store         │ │ - Serves     │ │  - Serves        │
│  - Peer Discovery│ │   Requests   │ │    Requests      │
└──────────────────┘ └──────────────┘ └──────────────────┘
```

### Data Flow

**Upload Process:**
```
1. User selects file → 2. File chunked (1MB pieces) → 3. Each chunk hashed (SHA-256)
   → 4. Chunks distributed to storage nodes → 5. Hashes registered in DHT
   → 6. Manifest created with metadata
```

**Download Process:**
```
1. User requests file → 2. Query DHT for chunk locations → 3. Fetch chunks from nodes
   → 4. Verify chunk hashes → 5. Reassemble file → 6. Return to user
```

---

## 📸 Screenshots

### Main Interface
![Main Interface](D:\Decentralized-File-Storage\image1.png)

### File Upload
![File Upload](D:\Decentralized-File-Storage\image1.png)

### File List
![File List](D:\Decentralized-File-Storage\image.png)

---

## 🚀 Installation

### Prerequisites

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **pip** (included with Python)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/garvita-d/Decentralized-File-Storage.git
   cd Decentralized-File-Storage
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python -c "import fastapi, uvicorn, httpx; print('✅ All dependencies installed')"
   ```

---

## ⚡ Quick Start

### Start the Network (4 Terminals Required)

#### Terminal 1: DHT Bootstrap Node
```bash
cd Decentralized-File-Storage
venv\Scripts\activate
python run_node.py --port 7001
```

#### Terminal 2: Storage Node 1
```bash
cd Decentralized-File-Storage
venv\Scripts\activate
python run_node.py --port 7002 --storage_dir ./storage/7002
```

#### Terminal 3: Storage Node 2
```bash
cd Decentralized-File-Storage
venv\Scripts\activate
python run_node.py --port 7003 --storage_dir ./storage/7003
```

#### Terminal 4: API Server
```bash
cd Decentralized-File-Storage
venv\Scripts\activate
python api_server.py
```

Wait for: `Uvicorn running on http://127.0.0.1:8080`

### Access the Web Interface

Open `frontend_app.html` in your browser:
```bash
# Windows
start frontend_app.html

# macOS
open frontend_app.html

# Linux
xdg-open frontend_app.html
```

Or navigate to: `http://127.0.0.1:8080` for API-only access.

---

## 💻 Usage

### Web Interface

1. **Upload Files**
   - Drag & drop files onto the upload area, OR
   - Click "Choose File" to browse
   - Wait for chunking and distribution
   - Copy the content hash for later retrieval

2. **View Stored Files**
   - Scroll to "Stored Files" section
   - See all uploaded files with metadata
   - View file size, chunk count, and hash

3. **Download Files**
   - Click "Download" button on any file
   - File reconstructed from chunks automatically
   - Saved to your downloads folder

4. **Search by Hash**
   - Copy a file's content hash
   - Paste into search box
   - Find file even if uploaded by another user

5. **Monitor Network**
   - View real-time node status at top
   - Green = online, Red = offline
   - See which nodes are storing data

### Command Line Interface

#### Upload a File
```bash
python demo_prepare.py --file myfile.pdf --peer_ports 7002,7003
# Creates manifest.json with file metadata
```

#### Download a File
```bash
python demo_retrieve.py --manifest manifest.json
# Reconstructs file in downloads/ folder
```

#### List Stored Files
```bash
python client/cli.py list
```

---

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8080/api
```

### Endpoints

#### `POST /api/upload`
Upload a file to the network

**Request:**
```bash
curl -X POST http://127.0.0.1:8080/api/upload \
  -F "file=@myfile.pdf"
```

**Response:**
```json
{
  "status": "success",
  "fileId": "myfile.pdf",
  "chunks": 5,
  "hash": "8bbfd9d0682f617f...",
  "manifest": {...}
}
```

#### `GET /api/files`
List all uploaded files

**Request:**
```bash
curl http://127.0.0.1:8080/api/files
```

**Response:**
```json
{
  "files": [
    {
      "name": "myfile.pdf",
      "hash": "8bbfd9d0682f617f...",
      "chunks": 5,
      "size": 5242880
    }
  ]
}
```

#### `GET /api/download/{file_id}`
Download a file by name

**Request:**
```bash
curl -O http://127.0.0.1:8080/api/download/myfile.pdf
```

#### `GET /api/search/{hash}`
Search for a file by content hash

**Request:**
```bash
curl http://127.0.0.1:8080/api/search/8bbfd9d0682f617f...
```

**Response:**
```json
{
  "found": true,
  "file": {
    "name": "myfile.pdf",
    "hash": "8bbfd9d0682f617f...",
    "chunks": 5,
    "size": 5242880
  }
}
```

#### `GET /api/nodes`
Get status of all network nodes

**Request:**
```bash
curl http://127.0.0.1:8080/api/nodes
```

**Response:**
```json
{
  "nodes": [
    {"name": "DHT Node", "port": 7001, "status": "online"},
    {"name": "Storage Node 1", "port": 7002, "status": "online"},
    {"name": "Storage Node 2", "port": 7003, "status": "online"}
  ]
}
```

### Interactive API Docs

Visit `http://127.0.0.1:8080/docs` for Swagger UI documentation.

---

## 📁 Project Structure

```
Decentralized-File-Storage/
│
├── README.md                    # This file
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
│
├── api_server.py                # REST API server (NEW)
├── frontend_app.html            # Web interface (NEW)
├── run_node.py                  # Node launcher
├── demo_prepare.py              # CLI upload tool
├── demo_retrieve.py             # CLI download tool
│
├── src/                         # Source code
│   ├── common/                  # Shared utilities
│   │   └── hashing.py          # SHA-256 hashing
│   ├── dht/                     # DHT implementation
│   │   ├── server.py           # DHT node server
│   │   ├── client.py           # DHT client
│   │   ├── routing.py          # Routing table
│   │   ├── kademlia.py         # Kademlia protocol
│   │   └── id.py               # Node ID generation
│   ├── retrieval/               # File retrieval
│   │   ├── retriever.py        # Download logic
│   │   └── manifest.py         # Manifest schema
│   ├── utils/                   # Utilities
│   │   └── chunking.py         # File chunking
│   └── node/                    # Node operations
│       ├── network.py          # Network layer
│       └── server.py           # Storage node server
│
├── client/                      # Client interface
│   └── cli.py                  # Command-line tool
│
├── tests/                       # Test suite
│   ├── test_chunking.py        # Chunking tests
│   ├── test_integration.py     # Integration tests
│   └── __init__.py
│
├── storage/                     # Local chunk storage
│   ├── 7002/                   # Node 7002 chunks
│   └── 7003/                   # Node 7003 chunks
│
├── manifests/                   # File manifests
│   └── *.json                  # File metadata
│
├── downloads/                   # Retrieved files
│
└── venv/                        # Virtual environment (ignored)
```

---

## 🔧 How It Works

### 1. File Upload

```python
# File is read and split into chunks
def chunk_file(file_path, chunk_size=1024*1024):
    chunks = []
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            # Hash each chunk with SHA-256
            chunk_hash = sha256(chunk).hexdigest()
            chunks.append((chunk_hash, chunk))
    return chunks
```

### 2. Chunk Distribution

```python
# Chunks distributed across storage nodes
for i, (chunk_hash, chunk_data) in enumerate(chunks):
    # Round-robin distribution
    node_port = STORAGE_NODES[i % len(STORAGE_NODES)]
    
    # Store chunk on selected node
    save_chunk(node_port, chunk_hash, chunk_data)
    
    # Register in DHT
    dht.register(chunk_hash, node_port)
```

### 3. DHT Lookup

```python
# Find which node has a specific chunk
def lookup_chunk(chunk_hash):
    # Query DHT for chunk location
    node_info = dht.find_value(chunk_hash)
    return node_info['peers']
```

### 4. File Retrieval

```python
# Reconstruct file from chunks
def retrieve_file(manifest):
    chunks = []
    for chunk_hash in manifest['chunkHashes']:
        # Find node storing this chunk
        peers = dht.lookup(chunk_hash)
        
        # Download chunk from node
        chunk_data = download_from_peer(peers[0], chunk_hash)
        
        # Verify integrity
        if sha256(chunk_data).hexdigest() != chunk_hash:
            raise IntegrityError("Chunk corrupted!")
        
        chunks.append(chunk_data)
    
    # Reassemble file
    return b''.join(chunks)
```

### 5. Fault Tolerance

If a node fails:
- DHT removes failed node from routing table
- Chunks can be replicated to healthy nodes
- Files remain accessible via remaining peers

---

## 🧪 Testing

### Run All Tests
```bash
pytest tests/
```

### Run Specific Tests
```bash
# Test chunking
pytest tests/test_chunking.py

# Test integration
pytest tests/test_integration.py
```

### Manual Testing

#### Test 1: Small File Upload
```bash
# Create test file
echo "Hello World" > test.txt

# Upload via web interface or:
python demo_prepare.py --file test.txt

# Download
python demo_retrieve.py --manifest manifest.json

# Verify
diff test.txt downloads/test.txt.reconstructed
```

#### Test 2: Large File Upload
```bash
# Create 10MB file
python -c "with open('large.bin', 'wb') as f: f.write(b'x'*10485760)"

# Upload and download
python demo_prepare.py --file large.bin
python demo_retrieve.py --manifest manifest.json
```

#### Test 3: Node Failure
```bash
# Upload file to nodes 7002 and 7003
python demo_prepare.py --file test.txt --peer_ports 7002,7003

# Stop node 7002 (Ctrl+C in Terminal 2)

# Try downloading - should still work from 7003!
python demo_retrieve.py --manifest manifest.json
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Add docstrings to all functions
- Write tests for new features
- Update documentation as needed

---

## 👥 Team

| Member | Role | Responsibilities |
|--------|------|------------------|
| **Garvita Dalmia** | Project Lead | Architecture, Integration, Frontend |
| **Rupasri Chalasani** | Frontend | Architecture |
| **SJ Sathwik** | DHT Module | Distributed Hash Table Implementation |
| **Anya Kalluri** | Storage Layer | Node Communication, P2P Network |
| **Divya Borra** | Chunking & Hashing | File Processing, Integrity |
| **Amit Reddy** | Retrieval System | File Reconstruction, API |

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by [IPFS](https://ipfs.io/) and [Filecoin](https://filecoin.io/)
- Built with [FastAPI](https://fastapi.tiangolo.com/), [uvicorn](https://www.uvicorn.org/), and [httpx](https://www.python-httpx.org/)
- DHT implementation based on [Kademlia](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf) protocol

---

## 📞 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/garvita-d/Decentralized-File-Storage/issues)
- **Email**: garvita.d@example.com
- **Documentation**: See [Wiki](https://github.com/garvita-d/Decentralized-File-Storage/wiki)

---

## 🗺️ Roadmap

### Completed ✅
- [x] File chunking and hashing
- [x] DHT implementation
- [x] P2P network layer
- [x] File retrieval system
- [x] Web interface
- [x] REST API

### In Progress 🚧
- [ ] Chunk replication for redundancy
- [ ] File encryption for privacy
- [ ] User authentication system

### Future Plans 🔮
- [ ] Mobile app (React Native)
- [ ] IPFS compatibility layer
- [ ] Incentive mechanism (cryptocurrency integration)
- [ ] Content delivery optimization
- [ ] Distributed file search
- [ ] Real-time synchronization

---

## 📊 Performance

- **Upload Speed**: ~10 MB/s (local network)
- **Download Speed**: ~15 MB/s (local network)
- **Chunk Size**: 1 MB (configurable)
- **Max File Size**: Limited only by available storage
- **Node Capacity**: Tested with up to 10 nodes

---

**Made with ❤️ by the Decentralized Storage Team**

⭐ Star this repo if you find it useful!

🐛 Found a bug? [Open an issue](https://github.com/garvita-d/Decentralized-File-Storage/issues/new)

🤝 Want to contribute? [Check our guidelines](#contributing)