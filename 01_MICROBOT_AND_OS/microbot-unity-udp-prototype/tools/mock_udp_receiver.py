import socket
from datetime import datetime

HOST = "0.0.0.0"
PORT = 4210

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print(f"[MicroBot UDP Mock Receiver] Listening on {HOST}:{PORT}")
print("Press CTRL+C to stop.")

try:
    while True:
        data, addr = sock.recvfrom(4096)
        timestamp = datetime.now().isoformat(timespec="seconds")
        text = data.decode("utf-8", errors="replace")
        print(f"[{timestamp}] From {addr}: {text}")
except KeyboardInterrupt:
    print("\n[MicroBot UDP Mock Receiver] Stopped.")
finally:
    sock.close()
