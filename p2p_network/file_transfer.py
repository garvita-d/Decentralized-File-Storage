import os, socket, json, hashlib
from message_protocol import send_json, recv_json

def send_chunk(conn, filepath):
    size = os.path.getsize(filepath)
    header = {"type": "CHUNK_RESPONSE", "content_length": size}
    send_json(conn, header)
    with open(filepath, "rb") as f:
        while (chunk := f.read(4096)):
            conn.sendall(chunk)

def receive_chunk(sock, dest_path):
    header = recv_json(sock)
    size = header["content_length"]
    data = b""
    while len(data) < size:
        chunk = sock.recv(min(4096, size - len(data)))
        if not chunk:
            break
        data += chunk
    with open(dest_path, "wb") as f:
        f.write(data)
    return hashlib.sha256(data).hexdigest()
