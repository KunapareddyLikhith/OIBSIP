import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

# Broadcast message to all clients
def broadcast(message, _client=None):
    for client in clients:
        if client != _client:
            client.send(message)

# Handle messages from a client
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} left the chat!".encode('utf-8'))
            break

# Receive clients
def receive():
    print(f"Server running on {HOST}:{PORT}...")
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client.send("Connected to server!".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()

    conn.sendall(msg.encode())

conn.close()

