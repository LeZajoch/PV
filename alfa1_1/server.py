import socket
import threading
import sys
import queue
import json
import hashlib
import os

# Load configuration from config.json
CONFIG_FILE = "config.json"
USERS_FILE = "users.json"


def create_default_config():
    default_config = {
        "host": "127.0.0.1",
        "port": 5000
    }
    with open(CONFIG_FILE, "w") as file:
        json.dump(default_config, file, indent=4)
    print(f"[CONFIG CREATED] Default {CONFIG_FILE} created.")


def create_default_users():
    default_users = {
        "admin": hash_password("padmin")
    }
    with open(USERS_FILE, "w") as file:
        json.dump(default_users, file, indent=4)
    print(f"[USERS CREATED] Default {USERS_FILE} created.")


def load_config():
    if not os.path.exists(CONFIG_FILE):
        create_default_config()
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)


def load_users():
    if not os.path.exists(USERS_FILE):
        create_default_users()
    with open(USERS_FILE, "r") as file:
        return json.load(file)


def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


config = load_config()
users = load_users()


class Server:
    def __init__(self):
        self.host = config['host']
        self.port = config['port']
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[SERVER STARTED] Listening on {self.host}:{self.port}")

    def broadcast(self, message, client_socket):
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message)
                except:
                    self.clients.remove(client)

    def handle_client(self, client_socket, client_address):
        print(f"[NEW CONNECTION] {client_address} connected.")
        client_socket.send(b"[LOGIN] Enter username:")
        username = client_socket.recv(1024).decode().strip()
        client_socket.send(b"[LOGIN] Enter password:")
        password = client_socket.recv(1024).decode().strip()

        if username in users and users[username] == hash_password(password):
            client_socket.send(b"[LOGIN SUCCESSFUL] Welcome!")
        else:
            client_socket.send(b"[LOGIN FAILED] Invalid credentials.")
            client_socket.close()
            return

        self.clients.append(client_socket)
        while True:
            try:
                message = client_socket.recv(1024)
                if message:
                    print(f"[{username}] {message.decode()}")
                    self.broadcast(f"[{username}] {message.decode()}".encode(), client_socket)
                else:
                    print(f"[DISCONNECTED] {username}")
                    self.clients.remove(client_socket)
                    client_socket.close()
                    break
            except:
                print(f"[ERROR] Connection lost with {username}")
                self.clients.remove(client_socket)
                client_socket.close()
                break

    def run(self):
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
        except KeyboardInterrupt:
            print("[SERVER SHUTDOWN] Server stopped.")
            self.server_socket.close()


class Client:
    def __init__(self):
        self.host = config['host']
        self.port = config['port']
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def register(self):
        print("[REGISTER] Create a new account.")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        users[username] = hash_password(password)
        save_users(users)
        print("[REGISTER] Account created successfully.")

    def send_message(self):
        try:
            while True:
                message = input("")
                if message.lower() == 'quit':
                    self.client_socket.close()
                    sys.exit()
                self.client_socket.send(message.encode())
        except KeyboardInterrupt:
            print("[CLIENT SHUTDOWN] Disconnected from server.")
            self.client_socket.close()
            sys.exit()

    def receive_message(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    print(message)
                else:
                    print("[SERVER SHUTDOWN] Server closed connection.")
                    self.client_socket.close()
                    break
            except:
                print("[ERROR] Lost connection to server.")
                self.client_socket.close()
                break


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["server", "client"]:
        print("Usage: python cmd_chat_app.py [server|client]")
        sys.exit()

    mode = sys.argv[1]
    if mode == "server":
        server = Server()
        server.run()
    elif mode == "client":
        client = Client()
        print("1. Register\n2. Login")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            client.register()
        threading.Thread(target=client.receive_message).start()
        client.send_message()


if __name__ == "__main__":
    main()
