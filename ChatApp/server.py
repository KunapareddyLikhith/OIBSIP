import socket

# Server setup
HOST = '127.0.0.1'   # localhost
PORT = 12345         # any free port

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server started on {HOST}:{PORT}, waiting for connection...")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")

while True:
    data = conn.recv(1024).decode()
    if not data:
        break
    print(f"Client: {data}")
    msg = input("Server: ")
    conn.sendall(msg.encode())

conn.close()
