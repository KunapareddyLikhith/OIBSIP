import socket

# Client setup
HOST = '127.0.0.1'   # server IP
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("Connected to the server. Type messages below:")

while True:
    msg = input("Client: ")
    client_socket.sendall(msg.encode())
    data = client_socket.recv(1024).decode()
    print(f"Server: {data}")
