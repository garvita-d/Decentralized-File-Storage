# server.py
import socket
import threading
import json

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    with conn:
        data = conn.recv(4096)
        if not data:
            return
        try:
            msg = json.loads(data.decode())
            print(f"[RECEIVED FROM {addr}] {msg}")
            response = {"status": "ok", "message": "received your data"}
            conn.sendall(json.dumps(response).encode())
        except Exception as e:
            print("Error:", e)

def start_server(host="0.0.0.0", port=5000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[LISTENING] Peer listening on {host}:{port}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
