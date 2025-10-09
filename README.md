\# Decentralized File Storage System



A peer-to-peer decentralized file storage system that distributes files across multiple nodes without relying on a central server. Built with Python and designed for fault tolerance and data integrity.



---



\## 📋 Table of Contents



\- \[Overview](#overview)

\- \[Features](#features)

\- \[Architecture](#architecture)

\- \[Team Members](#team-members)

\- \[Project Structure](#project-structure)

\- \[Installation](#installation)

\- \[Usage](#usage)

\- \[Development Workflow](#development-workflow)

\- \[Testing](#testing)

\- \[Roadmap](#roadmap)

\- \[Contributing](#contributing)

\- \[License](#license)



---



\## 🎯 Overview



This project implements a decentralized file storage system where:

\- Files are split into chunks and distributed across multiple nodes

\- Each chunk is identified by its SHA-256 hash

\- A Distributed Hash Table (DHT) tracks which nodes store which chunks

\- Files can be retrieved even if some nodes go offline

\- Data integrity is verified through cryptographic hashing



---



\## ✨ Features



\- \*\*File Chunking\*\*: Automatically splits large files into 1MB chunks

\- \*\*Content Addressing\*\*: Each chunk identified by SHA-256 hash

\- \*\*Peer-to-Peer Network\*\*: Nodes communicate directly without central server

\- \*\*Distributed Hash Table (DHT)\*\*: Efficient chunk location lookup

\- \*\*Data Integrity\*\*: Hash verification ensures no data corruption

\- \*\*Fault Tolerance\*\*: Retrieve files even if some nodes are offline

\- \*\*Simple CLI\*\*: Easy-to-use command-line interface



---



\## 🏗️ Architecture



```

┌─────────────┐

│   Client    │ ← User uploads/downloads files

└──────┬──────┘

&nbsp;      │

&nbsp;      ▼

┌─────────────────────────────────┐

│     File Chunking Module        │ ← Splits file into chunks

│  (SHA-256 hash each chunk)      │

└──────┬──────────────────────────┘

&nbsp;      │

&nbsp;      ▼

┌─────────────────────────────────┐

│  Distributed Hash Table (DHT)   │ ← Maps chunk\_hash → node\_addresses

└──────┬──────────────────────────┘

&nbsp;      │

&nbsp;      ▼

┌─────────────────────────────────┐

│    P2P Network Layer            │ ← Nodes communicate and store chunks

│  Node 1 | Node 2 | Node 3 ...   │

└─────────────────────────────────┘

```



\### How It Works



1\. \*\*Upload\*\*: File → Chunked → Hashed → Distributed to nodes → DHT updated

2\. \*\*Download\*\*: Query DHT → Locate chunks → Download from nodes → Verify hashes → Reassemble file



---



\## 👥 Team Members



| Member | Role | Responsibilities | Branch |

|--------|------|------------------|--------|

| \*\*Member 1\*\* | Chunking \& Hashing | File splitting, SHA-256 hashing, manifest creation | `chunking-hashing` |

| \*\*Member 2\*\* | P2P Network | Node communication, TCP sockets, message protocol | `p2p-network` |

| \*\*Member 3\*\* | DHT Module | Hash table implementation, chunk location tracking | `dht-module` |

| \*\*Member 4\*\* | File Retrieval | Chunk downloading, integrity verification, reassembly | `file-retrieval` |

| \*\*Member 5\*\* | Frontend/CLI | User interface, command-line tools, integration | `frontend` |



---



\## 📁 Project Structure



```

Decentralized-File-Storage/

│

├── README.md                 # Project documentation

├── requirements.txt          # Python dependencies

├── .gitignore               # Git ignore rules

├── LICENSE                  # MIT License

│

├── client/                  # Client interface

│   ├── \_\_init\_\_.py

│   ├── cli.py              # Command-line interface

│   └── retrieval.py        # File download logic

│

├── node/                    # Node server logic

│   ├── \_\_init\_\_.py

│   ├── network.py          # P2P communication

│   └── storage.py          # Local chunk storage

│

├── dht/                     # Distributed Hash Table

│   ├── \_\_init\_\_.py

│   └── dht.py              # DHT implementation

│

├── utils/                   # Helper functions

│   ├── \_\_init\_\_.py

│   ├── chunking.py         # File chunking logic

│   └── hashing.py          # SHA-256 hashing

│

├── frontend/                # Optional web interface

│   └── app.py              # Flask application

│

├── tests/                   # Test suite

│   ├── \_\_init\_\_.py

│   ├── test\_chunking.py

│   ├── test\_network.py

│   ├── test\_dht.py

│   └── test\_integration.py

│

└── chunks/                  # Local storage for chunks

&nbsp;   └── .gitkeep

```



---



\## 🚀 Installation



\### Prerequisites



\- Python 3.8 or higher

\- Git

\- pip (Python package manager)



\### Setup



1\. \*\*Clone the repository\*\*

&nbsp;  ```bash

&nbsp;  git clone https://github.com/garvita-d/Decentralized-File-Storage.git

&nbsp;  cd Decentralized-File-Storage

&nbsp;  ```



2\. \*\*Create a virtual environment\*\* (recommended)

&nbsp;  ```bash

&nbsp;  python -m venv venv

&nbsp;  

&nbsp;  # On Windows

&nbsp;  venv\\Scripts\\activate

&nbsp;  

&nbsp;  # On macOS/Linux

&nbsp;  source venv/bin/activate

&nbsp;  ```



3\. \*\*Install dependencies\*\*

&nbsp;  ```bash

&nbsp;  pip install -r requirements.txt

&nbsp;  ```



4\. \*\*Verify installation\*\*

&nbsp;  ```bash

&nbsp;  python -m pytest tests/

&nbsp;  ```



---



\## 💻 Usage



\### Starting a Node



```bash

python node/network.py --port 8000

```



\### Uploading a File



```bash

python client/cli.py upload myfile.pdf

\# Returns: File hash for retrieval

```



\### Downloading a File



```bash

python client/cli.py download <file\_hash> --output restored\_file.pdf

```



\### Running Multiple Nodes (for testing)



```bash

\# Terminal 1

python node/network.py --port 8000



\# Terminal 2

python node/network.py --port 8001



\# Terminal 3

python node/network.py --port 8002

```



---



\## 🔧 Development Workflow



\### Branching Strategy



\- `main` → Production-ready code (protected)

\- `dev` → Integration branch for testing

\- `feature-branches` → Individual module development



\### Working on Your Feature



1\. \*\*Ensure you're on your feature branch\*\*

&nbsp;  ```bash

&nbsp;  git checkout <your-branch-name>

&nbsp;  git pull origin dev  # Get latest changes

&nbsp;  ```



2\. \*\*Make your changes\*\*

&nbsp;  ```bash

&nbsp;  # Code your module

&nbsp;  ```



3\. \*\*Test your code\*\*

&nbsp;  ```bash

&nbsp;  pytest tests/test\_your\_module.py

&nbsp;  ```



4\. \*\*Commit and push\*\*

&nbsp;  ```bash

&nbsp;  git add .

&nbsp;  git commit -m "Descriptive commit message"

&nbsp;  git push origin <your-branch-name>

&nbsp;  ```



5\. \*\*Create a Pull Request\*\*

&nbsp;  - Go to GitHub repository

&nbsp;  - Click "Pull requests" → "New pull request"

&nbsp;  - Base: `dev`, Compare: `<your-branch-name>`

&nbsp;  - Request review from teammates

&nbsp;  - Merge after approval



\### Code Review Checklist



\- \[ ] Code follows Python PEP 8 style guide

\- \[ ] All tests pass

\- \[ ] No hardcoded values (use constants or config)

\- \[ ] Functions have docstrings

\- \[ ] Error handling implemented

\- \[ ] No merge conflicts with `dev`



---



\## 🧪 Testing



\### Run All Tests



```bash

pytest tests/

```



\### Run Specific Test File



```bash

pytest tests/test\_chunking.py

```



\### Run with Coverage



```bash

pytest --cov=. tests/

```



\### Integration Testing



```bash

\# Start multiple nodes and run integration tests

python tests/test\_integration.py

```



---



\## 🗓️ Roadmap



\### Week 1: Foundation

\- \[x] Repository setup

\- \[x] Project structure

\- \[ ] File chunking module

\- \[ ] Basic CLI interface



\### Week 2: Networking

\- \[ ] P2P network implementation

\- \[ ] DHT module

\- \[ ] Node communication protocol



\### Week 3: Retrieval \& Integration

\- \[ ] File retrieval module

\- \[ ] Hash verification

\- \[ ] Module integration testing



\### Week 4: Testing \& Polish

\- \[ ] Fault tolerance testing

\- \[ ] Performance optimization

\- \[ ] Documentation finalization



\### Week 5: Enhancements (Optional)

\- \[ ] Chunk replication

\- \[ ] File encryption

\- \[ ] Web-based interface

\- \[ ] Incentive mechanism simulation



---



\## 🤝 Contributing



1\. Choose an issue from the \[Issues](../../issues) page

2\. Assign yourself to the issue

3\. Create/switch to your feature branch

4\. Implement the feature with tests

5\. Submit a Pull Request

6\. Request code review

7\. Address feedback and merge



\### Commit Message Guidelines



\- Use present tense: "Add feature" not "Added feature"

\- Be descriptive: "Implement SHA-256 hashing for chunks"

\- Reference issues: "Fix #12: Handle empty file upload"



---



\## 📄 License



This project is licensed under the MIT License - see the \[LICENSE](LICENSE) file for details.



---



\## 📞 Contact \& Support



\- \*\*Issues\*\*: Report bugs or request features via \[GitHub Issues](../../issues)

\- \*\*Discussions\*\*: Use \[GitHub Discussions](../../discussions) for questions

\- \*\*Project Board\*\*: Track progress on our \[Project Board](../../projects)



---



\## 🙏 Acknowledgments



\- Inspired by decentralized storage systems like IPFS and Filecoin

\- Built as a learning project for distributed systems concepts

\- Thanks to our amazing team of 5 developers!



---



\*\*Happy Coding! 🚀\*\*

