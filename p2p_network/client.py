# client.py
import socket, json

def send_message(ip, port, msg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(json.dumps(msg).encode())
        data = s.recv(4096)
        print("[RESPONSE]", data.decode())

if __name__ == "__main__":
    send_message("127.0.0.1", 5000, {"type": "HELLO", "payload": "Hi Peer!"})
