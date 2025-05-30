import socket
import threading

HOST = '127.0.0.2'
PORT = 12345
clients = {}

def broadcast(message, sender_socket=None):
    for username, client_socket in clients.items():
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                client_socket.close()

def handle_client(client_socket, addr):
    try:
        client_socket.send('Enter your username:'.encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8').strip()
        
        while username in clients:
            client_socket.send('Username taken. Enter a new username: '.encode('utf-8'))
            username = client_socket.recv(1024).decode('utf-8').strip()
        
        clients[username] = client_socket
        print(f"{username} connected from {addr}")
        
        # Add a newline after receiving the username to separate it from subsequent messages
        # This helps ensure the client's next prompt or message display starts on a new line.
        client_socket.send('\n'.encode('utf-8'))

        # Broadcast the join message to *other* clients first
        broadcast(f"{username} has joined the chat.", client_socket)
        
        # Send the welcome message specifically to the newly connected client
        client_socket.send("You are connected. Type /list to see users.\n".encode('utf-8'))

        while True:
            msg = client_socket.recv(1024).decode('utf-8')
            if msg.strip() == '/list':
                user_list = '; '.join(clients.keys())
                client_socket.send(f"Connected users: {user_list}\n".encode('utf-8'))
            elif msg.strip().lower() == '/quit':
                break
            else:
                broadcast(f"{username}: {msg}", client_socket)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if username in clients:
            print(f"{username} disconnected.")
            broadcast(f"{username} has left the chat.")
            clients.pop(username, None)
            client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server started on {HOST}:{PORT}")
    
    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()