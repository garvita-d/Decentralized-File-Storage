import json, struct

def send_json(sock, obj):
    data = json.dumps(obj).encode()
    sock.sendall(struct.pack("!I", len(data)))
    sock.sendall(data)

def recv_json(sock):
    header = sock.recv(4)
    if not header:
        return None
    length = struct.unpack("!I", header)[0]
    data = b""
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk
    return json.loads(data.decode())
