import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
clients = {}
lock = threading.Lock()

def broadcast(message, sender_socket=None):
    with lock:
        for client_socket in clients.keys():
            if client_socket != sender_socket:
                try:
                    client_socket.send(message)
                except:
                    client_socket.close()
                    del clients[client_socket]

def handle_client(client_socket, client_address):
    username = client_socket.recv(1024).decode('utf-8')
    with lock:
        clients[client_socket] = username

    broadcast(f"{username} has joined the chat.\n".encode('utf-8'))
    print(f"[DEBUG] {username} connected from {client_address}")

    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                formatted_message = f"{username}: {message.decode('utf-8')}\n"
                print(f"[DEBUG] {formatted_message.strip()}")
                broadcast(formatted_message.encode('utf-8'), sender_socket=client_socket)
            else:
                raise Exception("Empty message received")
        except:
            with lock:
                del clients[client_socket]
            broadcast(f"{username} has left the chat.\n".encode('utf-8'))
            print(f"[DEBUG] {username} disconnected.")
            break

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server started, listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

start_server()
